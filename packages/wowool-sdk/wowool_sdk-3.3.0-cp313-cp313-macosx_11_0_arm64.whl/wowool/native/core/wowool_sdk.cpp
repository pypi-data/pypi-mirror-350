//////////////////////////////////////
// Warning Do not move this headers.
// Otherwise MSVC can not compile the stuff
/////////////////////////////////////////////////////////////////
#define WITH_THREAD
#include <Python.h>
#include <chrono>
#include <iostream>
#include <mutex>
#include <pybind11/functional.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>
#include <string>
#include <thread>
#include <variant>
#include <vector>
#include "eot/analyzer/analyzer.hpp"
#include "eot/analyzer/options.hpp"
#include "eot/common/Exception.hpp"
#include "eot/common/Logging.hpp"
#include "eot/common/options.hpp"
#include "eot/common/version.hpp"
#include "eot/domain/domain.hpp"
#include "eot/engine/engine.hpp"
#include "eot/filter/filter.hpp"
#include "eot/language_identifier/language_identifier.hpp"
#if !defined(WIN32)
	#include <signal.h>
#else
	#include <thread>
	#include <windows.h>
#endif
namespace py = pybind11;
using namespace std::chrono_literals;

//#define DEBUG_WOW_THREADS

#define TIR_WLOG_COMPILER 0x1000

std::mutex global_python_mutex;
#define PYTHON_LOCK std::lock_guard<std::mutex> guard(global_python_mutex);

// std::string get_environment(std::string const &env_id, std::string const default_value)
// {
// 	char const *value_ptr = std::getenv(env_id.c_str());
// 	if (value_ptr)
// 	{
// 		return value_ptr;
// 	}
// 	return default_value;
// }

bool get_environment_bool(std::string const &env_id, bool default_value)
{
	char const *value_ptr = std::getenv(env_id.c_str());
	if (value_ptr)
	{
		std::string value(value_ptr);
		return value == "true" or value == "True";
	}
	return default_value;
}

bool lock_gil = get_environment_bool("WOWOOL_LOCK_GIL", false);

namespace detail {
	struct DoNotExecFirstTime
	{
		mutable bool initial = true;

		template<typename Functor>
		void operator()(Functor functor) const
		{
			if (!initial)
			{
				functor();
			}
			else
				initial = false;
		}

		void reset() { initial = true; }
	};

	std::string load(const char *filename)
	{
		std::string return_value;
		try
		{
			std::ifstream ifile(filename, std::ios_base::binary);
			ifile.exceptions(std::ios::badbit | std::ios::failbit | std::ios::eofbit);

			ifile.seekg(0, std::ios_base::end);
			size_t buffersize = ifile.tellg();
			std::vector<char> buffer(buffersize);

			ifile.seekg(0, std::ios_base::beg);
			ifile.read(&buffer[0], buffersize);

			std::copy(buffer.begin(), buffer.end(), std::back_inserter(return_value));
		} catch (std::exception const &ex)
		{
			std::stringstream error;
			error << "can not open file " << filename;
			throw std::runtime_error(error.str().c_str());
		}

		return return_value;
	}

	//#TODO: This can probably be removed. std::string has implicit char *
	// constructor
	std::string load(std::string const &filename) { return load(filename.c_str()); }

	///////////////////////////////////////////////////////////////////////////////////
	struct IInputProvider
	{
		virtual std::string const &type() const = 0;
		virtual std::string const &get_id() const = 0;
		virtual std::string const get_data() const = 0;
		virtual size_t size() const = 0;
		virtual ~IInputProvider() {}
	};

	struct StringProvider : IInputProvider
	{
		StringProvider(std::string const &d);
		StringProvider(std::string const &sid, std::string const &d);
		static const std::string object_type;

		std::string const &type() const { return object_type; }

		std::string const &get_id() const;
		std::string const get_data() const;
		size_t size() const;

		std::string id;
		std::string data;
	};

	struct FileProvider : IInputProvider
	{
		FileProvider(std::string const &filename);

		static const std::string object_type;

		std::string const &type() const { return object_type; }
		std::string const &get_id() const;
		std::string const get_data() const;
		size_t size() const;

		std::string id;
	};

	typedef std::shared_ptr<IInputProvider> InputProviderPtr;

	///////////////////////////////////////////////////////////////////////////////////

	struct InputPool
	{
		typedef std::vector<InputProviderPtr> input_provider_type;
		typedef input_provider_type::const_iterator const_iterator;
		typedef input_provider_type::const_iterator iterator;

		typedef std::tuple<std::string, InputProviderPtr, bool> thread_mime_type;
		typedef std::shared_ptr<thread_mime_type> thread_data_ptr;
		typedef std::vector<thread_data_ptr> output_provider_type;

		input_provider_type input_provider;
		output_provider_type output_provider;

		const_iterator begin() const { return input_provider.begin(); }
		const_iterator end() const { return input_provider.end(); }

		iterator begin() { return input_provider.begin(); }
		iterator end() { return input_provider.end(); }

		void add_data(std::string const &data);
		void add_data(std::string const &sid, std::string const &data);

		void add_file(std::string const &data);
		thread_data_ptr get();

		size_t size() const { return input_provider.size(); }

		void clear()
		{
			input_provider.clear();
			output_provider.clear();
		}
	};

	///////////////////////////////////////////////////////////////////////////////////

	static std::mutex access;
	static std::hash<std::string> StringHasher;
	static std::string make_uuid(std::string const &str)
	{
		std::stringstream id;
		id << "stream_" << StringHasher(str);
		return id.str();
	}

	StringProvider::StringProvider(std::string const &sid, std::string const &d)
		: id(sid), data(d) {}

	StringProvider::StringProvider(std::string const &d)
		: id(make_uuid(d)), data(d) {}

	size_t StringProvider::size() const { return data.length(); }

	std::string const StringProvider::object_type = "si";

	std::string const &StringProvider::get_id() const { return id; }

	std::string const StringProvider::get_data() const { return data; }

	std::string const FileProvider::object_type = "fi";

	FileProvider::FileProvider(std::string const &filename)
		: id(filename) {}

	std::string const &FileProvider::get_id() const { return id; }

	std::string const FileProvider::get_data() const { return load(id); }

	size_t FileProvider::size() const
	{
		std::ifstream ifile(get_id());
		ifile.seekg(0, std::ios_base::end);
		size_t sz = ifile.tellg();
		return sz;
	}

	void InputPool::add_data(std::string const &sid, std::string const &data)
	{
		std::lock_guard<std::mutex> guard(access);
		input_provider.emplace_back(new StringProvider(sid, data));
	}
	void InputPool::add_data(std::string const &data)
	{
		std::lock_guard<std::mutex> guard(access);
		input_provider.emplace_back(new StringProvider(data));
	}

	void InputPool::add_file(std::string const &data)
	{
		std::lock_guard<std::mutex> guard(access);
		input_provider.emplace_back(new FileProvider(data));
	}

	InputPool::thread_data_ptr InputPool::get()
	{
		std::lock_guard<std::mutex> guard(access);
		if (input_provider.empty())
			return thread_data_ptr();

		InputProviderPtr inprv = input_provider.front();
		input_provider.erase(input_provider.begin());
		thread_data_ptr ret = thread_data_ptr(new thread_mime_type("", inprv, false));
		output_provider.push_back(ret);
		return ret;
	}

} // namespace detail

std::ostream &print_string_map(std::ostream &out, eot::common::Options const &options)
{
	for (auto const &option : options)
	{
		out << option.first << ":" << option.second << ",";
	}
	return out;
}

namespace tir {
namespace pywowool {

	class exception_t : public std::exception
	{
	private:
		std::string message;
		std::string extraData;

	public:
		exception_t(std::string message_, std::string extraData_)
			: message(message_), extraData(extraData_) {}
		// TODO: declare this nothrow
		~exception_t() throw() {}
		const char *what() const throw() { return message.c_str(); }
		std::string getMessage() { return message; }
		std::string getExtraData() { return extraData; }
	};

	class exception_json_t : public std::exception
	{
	private:
		std::string json_data;

	public:
		exception_json_t(std::string json_data_)
			: json_data(json_data_) {}
		// TODO: declare this nothrow
		~exception_json_t() throw() {}
		const char *what() const throw() { return json_data.c_str(); }
	};

	void translate(exception_json_t const &e)
	{
		PyErr_SetString(PyExc_RuntimeError, e.what());
	}
	void translate(exception_t const &e)
	{
		PyErr_SetString(PyExc_RuntimeError, e.what());
	}

	eot::common::Options convert_py_2_api_options(py::dict const &kwargs)
	{
		eot::common::Options options;
		for (auto const &item : kwargs)
		{
			options.emplace(py::str(item.first), py::str(item.second));
		}
		return options;
	}

	std::string convert_filterset(eot::filter::Filter const &filterset)
	{
		return filterset.info();
	}

	py::dict convert_options_2_py(eot::common::Options const &options)
	{
		py::dict kwargs;
		for (auto const &item : options)
		{
			kwargs[py::str(item.first)] = py::str(item.second);
		}
		return kwargs;
	}

	// self.options["pytryoshka"] = "true"

	static eot::common::Options global_shared_engine_options = {
		{std::string("language"), std::string("auto")},
		// { std::string("verbose")  , std::string("trace") },
		{std::string("pytryoshka"), std::string("true")}};

	static std::shared_ptr<eot::engine::Engine>
		global_shared_engine; //( global_shared_engine_options );

	eot::engine::Engine &get_default_engine(eot::common::Options &options)
	{
		PYTHON_LOCK

		if (!global_shared_engine)
		{
			eot::engine::Engine *global_wowool_engine = new eot::engine::Engine(options);
			// std::cout << " !!!!!!!!!!!!!! Creating Global Engine" << global_wowool_engine << std::endl;
			global_shared_engine.reset(global_wowool_engine);
		}
		return *global_shared_engine;
	}

	class engine_t : public eot::engine::Engine
	{
	public:
		// typedef wowool::EngineInterface type;

		typedef eot::engine::Engine type;

		// using eot::engine::Engine::Engine;

		// engine_t(eot::engine::Engine const &&base)
		// 	: eot::engine::Engine(std::move(base))
		// {
		// 	std::cout << "PLUGIN eot::engine::Engine(eot::engine::Engine const &&base)" << this << std::endl;
		// }

		// engine_t(eot::engine::Engine const &&base, py::dict const &kwarg)
		// 	: eot::engine::Engine(tir::pywowool::convert_py_2_api_options(kwarg))
		// {
		// 	std::cout << "PLUGIN eot::engine::Engine(eot::engine::Engine const &&base, py::dict const &kwarg)" << this << std::endl;
		// }

		// we need this one to be able to create multi_process objects.
		engine_t(py::dict const &kwarg)
			: eot::engine::Engine(tir::pywowool::convert_py_2_api_options(kwarg))
		{
		}
	};

	class lid_t : public eot::language_identifier::LanguageIdentifier
	{
	public:
		typedef eot::language_identifier::LanguageIdentifier type;

		using eot::language_identifier::LanguageIdentifier::LanguageIdentifier;

		lid_t(eot::language_identifier::LanguageIdentifier const &&base)
			: eot::language_identifier::LanguageIdentifier(std::move(base)) {}

		lid_t(eot::analyzer::Engine const &engine, py::dict const &kwarg)
			: eot::language_identifier::LanguageIdentifier(engine, tir::pywowool::convert_py_2_api_options(kwarg)) {}

		lid_t(py::dict const &kwarg)
			: eot::language_identifier::LanguageIdentifier(tir::pywowool::get_default_engine(global_shared_engine_options), tir::pywowool::convert_py_2_api_options(kwarg)) {}
	};

	class domain_t : public eot::domain::Domain
	{
	public:
		typedef eot::domain::Domain type;

		using eot::domain::Domain::Domain;

		domain_t(eot::domain::Domain const &&base)
			: eot::domain::Domain(std::move(base)) {}

		domain_t(eot::analyzer::Engine const &engine, std::string const domain_descriptor, py::dict const &kwarg)
			: eot::domain::Domain(engine, domain_descriptor, tir::pywowool::convert_py_2_api_options(kwarg)) {}

		// we need this one to be able to create multi_process objects.
		domain_t(py::dict const &kwarg)
			: eot::domain::Domain(
				tir::pywowool::get_default_engine(global_shared_engine_options),
				kwarg["name"].cast<std::string>(),
				tir::pywowool::convert_py_2_api_options(kwarg)) {}

		// eot::analyzer::Results process(eot::analyzer::Results const document)
		// {
		// 	char *p = 0;
		// 	*p = 0;
		// 	std::cout << "PLUGIN domain_t::process" << std::endl;
		// 	// py::gil_scoped_release release; // Release the GIL
		// 	return (*static_cast<eot::domain::Domain const *>(this))(document);
		// };
	};

	eot::filter::FilterCollection string2filterset(std::string const &filter_str)
	{
		auto filter_vector = eot::common::split(filter_str, ',');
		return eot::filter::FilterCollection(filter_vector.begin(), filter_vector.end());
	}

	class filter_t : public eot::filter::Filter
	{
	public:
		typedef eot::filter::Filter type;

		using eot::filter::Filter::Filter;

		filter_t(eot::filter::Filter const &&base)
			: eot::filter::Filter(std::move(base)) {}

		filter_t(eot::filter::FilterCollection const &filterset)
			: eot::filter::Filter(filterset), _filterset(filterset) {}

		filter_t(std::string const filterset)
			: eot::filter::Filter(filterset), _filterset(string2filterset(filterset)) {}

		eot::filter::FilterCollection const _filterset;
	};

	class results_t : public eot::analyzer::Results
	{
	public:
		typedef eot::analyzer::Results type;

		using eot::analyzer::Results::Results;

		results_t(eot::analyzer::Results const &&base)
			: eot::analyzer::Results(std::move(base)) {}
	};

	class analyzer_t : public eot::analyzer::Analyzer
	{
	public:
		typedef eot::analyzer::Analyzer type;
		py::dict _kwargs;

		using eot::analyzer::Analyzer::Analyzer;
		using eot::analyzer::Analyzer::operator();

		analyzer_t(eot::analyzer::Analyzer const &&base)
			: eot::analyzer::Analyzer(std::move(base)) {}

		analyzer_t(eot::analyzer::Engine const &engine, py::dict const &kwarg)
			: eot::analyzer::Analyzer(engine, tir::pywowool::convert_py_2_api_options(kwarg)), _kwargs(kwarg) {}

		std::string process_return_string(std::string const &document, eot::common::Options const &json_options)
		{
			std::string ret_val;
			// std::cout << "options:" ; print_string_map(std::cout , json_options);
			// std::cout << std::endl;
			auto results = (*this)(document, json_options);
			return results.to_json();
		}
	};

	std::string pipeline_expand(std::string const &pipeline, std::string const &paths_str, bool file_access, bool allow_dev_versions, std::string const &pipeline_language)
	{
		try
		{
			std::vector<std::string> paths = eot::common::split(paths_str, ',');
			return eot::engine::expand_pipeline(pipeline, paths, file_access, allow_dev_versions, pipeline_language);
		} catch (eot::common::JsonException const &ex)
		{
			throw exception_json_t(ex.what());
		}
	}

	bool is_valid_version_format(std::string const &version)
	{
		return eot::common::is_valid_version_format(version);
	}

	std::string get_domain_info(std::string const domains_str)
	{
		std::vector<std::string> all_groups;
		std::vector<std::string> domains = eot::common::split(domains_str, ',');
		std::stringstream json;
		try
		{
			for (auto const &domain_descriptor : domains)
			{
				std::vector<std::string> groups;
				std::string domain = domain_descriptor;
				eot::domain::get_domain_concepts(domain, groups);
				std::copy(groups.begin(), groups.end(), std::back_inserter(all_groups));
			}
		} catch (std::exception const &ex)
		{
			throw exception_t(ex.what(), "");
		}

		if (!all_groups.empty())
		{
			json << "[";
			detail::DoNotExecFirstTime dneft;
			for (auto const &concept : all_groups)
			{
				if (concept.empty())
					continue;

				dneft([&json]() { json << ","; });
				json << "\"" << concept << "\"";
			}
			json << "]";
			return json.str();
		}
		else
		{
			json << "[]";
		}
		return json.str();
	}

	void print_log_message(unsigned short id, char const *msg)
	{
		std::cout << msg << std::endl;
	}

	std::string compile_domain(std::string const domain_descriptor, py::dict const &kwargs)
	{
		try
		{
			auto options = convert_py_2_api_options(kwargs);
			return eot::domain::compile_domain(options);
		} catch (eot::common::Exception &ex)
		{
			throw exception_t(ex.what(), "");
		} catch (std::exception const &e)
		{
			throw exception_t(e.what(), "");
		}
	}

	typedef std::vector<std::pair<std::string, std::string>> JsonCollectionType;

	struct JsonResultCollector
	{
		std::mutex access;
		JsonCollectionType results;

		void add(std::string const &id, std::string const &json_data)
		{
			std::lock_guard<std::mutex> guard(access);
			results.emplace_back(id, json_data);
		}
	};

	static int count = 0;
	struct ThreadData
	{
		analyzer_t &analyzer;
		std::vector<domain_t> domains;
		filter_t &filter;
		eot::common::Options json_options;
		detail::InputPool &ipp;
		JsonResultCollector &jsc;
		bool &continue_loop;

		ThreadData(analyzer_t &analyzer_, std::vector<domain_t> &domains_, filter_t &filter_, eot::common::Options const &json_options_, detail::InputPool &ipp_, JsonResultCollector &jsc_, bool &continue_loop_)
			: analyzer(analyzer_), domains(domains_), filter(filter_), json_options(json_options_), ipp(ipp_), jsc(jsc_), continue_loop(continue_loop_) {}

		void operator()()
		{
			while (continue_loop)
			{
				detail::InputPool::thread_data_ptr ip = ipp.get();
				if (!ip)
				{
					// std::this_thread::sleep_for(500ms);
					std::this_thread::yield();
					continue;
				}

				auto const &strid = std::get<1>(*ip)->get_id();
				auto const &strdata = std::get<1>(*ip)->get_data();

				try
				{
					count++;

#ifdef DEBUG_WOW_THREADS
					{
						std::stringstream strm;
						strm << "Data cpp:" << count << "(" << strid << ")" << std::endl;
						std::cerr << strm.str();
					}
#endif

					json_options[eot::analyzer::option::document_id] = strid;
					eot::analyzer::Results document = analyzer(strdata, json_options);
					for (auto const &domain : domains)
					{
						document = domain(document);
					}

					filter(document);
					std::string results = document.to_json();

#ifdef DEBUG_WOW_THREADS
					// {
					//     std::stringstream strm;
					//     strm << "Adding cpp:" << count << "(" << strid << ")" <<
					//     std::endl; std::cerr << strm.str();
					// }

#endif
					jsc.add(strid, results);
					if (!continue_loop)
						return;
				} catch (eot::common::Exception const &ex)
				{
					std::cerr << ex.what() << std::endl;
					std::stringstream error;
					error << "wow::exception in [" << strid << "]" << ex.what()
						  << std::endl;
					std::cerr << error.str();
				} catch (std::exception const &ex)
				{
					std::stringstream error;
					error << "std::exception in [" << strid << "]" << ex.what()
						  << std::endl;
					std::cerr << error.str();
					// continue_loop = false;
				}
			}
		}
	};

	typedef std::vector<std::pair<std::string, std::string>>
		InputProviderCollectionType;

	struct CallerThreadData
	{
		// InputProviderCollectionType ipc;
		detail::InputPool input_provider_pool;
		std::vector<std::thread> threads;
		bool continue_loop = true;
		JsonResultCollector jrc;
	};

	thread_local CallerThreadData call_thread_data;

	void exit_program(int sig);

	void mt_create_pool(analyzer_t &analyzer, std::vector<domain_t> &domains, filter_t &filter, py::dict const &kwargs, int nr_of_threads)
	{
		if (call_thread_data.threads.empty())
		{
			call_thread_data.continue_loop = true;
#if !defined(WIN32)
			(void)signal(SIGINT, exit_program);
#else
			SetConsoleCtrlHandler((PHANDLER_ROUTINE)exit_program, TRUE);
#endif
			// PyEval_InitThreads();
			// PyEval_ReleaseLock();
#ifdef DEBUG_WOW_THREADS
			std::cout << "Create Threads:" << nr_of_threads << std::endl;
#endif
			auto options = tir::pywowool::convert_py_2_api_options(kwargs);
			for (int i = 0; i < nr_of_threads; ++i)
			{
				ThreadData td(analyzer, domains, filter, options, call_thread_data.input_provider_pool, call_thread_data.jrc, call_thread_data.continue_loop);
				call_thread_data.threads.push_back(std::thread(td));
			}
		}
	}

	void mt_close_pool()
	{
#ifdef DEBUG_WOW_THREADS
		std::cout << "Closing Threads:" << std::endl;
#endif
		call_thread_data.continue_loop = false;
		for (auto &thread : call_thread_data.threads)
		{
			thread.join();
#ifdef DEBUG_WOW_THREADS
			std::cout << " --- closing Thread:" << std::endl;
#endif
		}
		call_thread_data.input_provider_pool.clear();
		call_thread_data.threads.clear();
		call_thread_data.jrc.results.clear();

#ifdef DEBUG_WOW_THREADS
		std::cout << " DONE Closing" << std::endl;
#endif
		call_thread_data.continue_loop = true;
	}

	void exit_program(int sig)
	{
		std::cout << "Ctrl-C\n";
		mt_close_pool();
		exit(-1);
	}

	JsonCollectionType process_input_provider(py::dict const &kwargs, int nr_of_threads, int batch_size, py::iterator collection_iterator)
	{
#ifdef DEBUG_WOW_THREADS
		std::cout << "DEBUG:THREADS:BATCH:" << std::endl;
#endif

		// py::object next = pyipc.attr("next");
		call_thread_data.jrc.results.clear();

		size_t count = 0;

		while (collection_iterator != py::iterator::sentinel())
		{
			auto const &ip = *collection_iterator;
			if (ip.is_none())
				break;
			count++;
#ifdef DEBUG_WOW_THREADS
			std::cout << "DEBUG:THREADS:count:" << count << std::endl;
#endif

			// std::cout << "count:" << count << std::endl;
			py::object _id = ip.attr("id");
			py::object _text = ip.attr("text");
			const std::string &data = py::str(_text);
			call_thread_data.input_provider_pool.add_data(py::str(_id), data);
			collection_iterator++;
		}

		while (call_thread_data.jrc.results.size() < count)
		{
#ifdef DEBUG_WOW_THREADS
			// std::cout << "Waiting yield ..." << call_thread_data.jrc.results.size()
			// << "/" << count << std::endl;
#endif
			std::this_thread::yield();
		}
		return call_thread_data.jrc.results;
	}

	JsonCollectionType process_list(py::dict const &kwargs, int nr_of_threads, int batch_size, const std::vector<std::string> &data)
	{
		call_thread_data.jrc.results.clear();
		call_thread_data.input_provider_pool.clear();

		size_t count = 0;
		int collected_batch_size = 0;

		auto it = data.begin();
		int i = 0;
		while (collected_batch_size < batch_size)
		{
			if (it == data.end())
				break;
			count++;
			const std::string &text = *it;
			collected_batch_size += text.length();
			std::stringstream id;
			id << i;
#ifdef DEBUG_WOW_THREADS
			std::cout << "ADD_data" << std::endl;
#endif
			call_thread_data.input_provider_pool.add_data(id.str(), text);
			it++;
			i++;
		}

		while (call_thread_data.jrc.results.size() < count)
		{
#ifdef DEBUG_WOW_THREADS
			// std::cout << "Waiting yield ..." << call_thread_data.jrc.results.size()
			// << "/" << count << std::endl;
#endif
			std::this_thread::yield();
		}
		return call_thread_data.jrc.results;
	}
	struct options_t
	{
		static const std::string language;
	};

	const std::string options_t::language = eot::analyzer::option::language;

	void __init__callback(py::module &) {}

	auto __exit__callback = []() {
		PYTHON_LOCK
		global_shared_engine.reset();
	};

	struct PyLog
	{
		std::function<void(unsigned short, const char *)> logit;

		PyLog(std::function<void(unsigned short, const char *)> logit_)
			: logit(logit_) {}
	};

	std::function<void(int, std::string)> pylogit;

	void global_logger_fn(unsigned short id, const char *msg)
	{
		if (pylogit)
		{
			pylogit(id, std::string(msg));
		}
	}

	void add_logger(unsigned short id, std::string level, const std::function<void(int, std::string)> logit)
	{
		pylogit = logit;
		eot::logging::add_logger(id, level, global_logger_fn);
	}

	void unset_logger() { pylogit = nullptr; }

}
} // namespace tir::pywowool

// clang-format off

std::variant<py::none, py::object> make_py_range(plugin_Annotation * concept_internal_ptr)
{
	if (concept_internal_ptr == 0)
	{
		return py::none();
	}
	py::module plugin = py::module::import("wowool.package.lib.wowool_plugin");
	auto annotation_range =  plugin.attr("annotation_range");
	return annotation_range(concept_internal_ptr);
}

PYBIND11_MODULE(_wowool_sdk, m)
{

    tir::pywowool::__init__callback(m);
    m.add_object("_cleanup", py::capsule(tir::pywowool::__exit__callback));
    m.def("get_domain_info", tir::pywowool::get_domain_info);
    m.def("pipeline_expand", tir::pywowool::pipeline_expand);
    m.def("is_valid_version_format", tir::pywowool::is_valid_version_format);
    m.def("compile_domain", tir::pywowool::compile_domain);
    m.def("process_input_provider", tir::pywowool::process_input_provider);
    m.def("process_list", tir::pywowool::process_list);
    m.def("mt_create_pool", tir::pywowool::mt_create_pool);
    m.def("mt_close_pool", tir::pywowool::mt_close_pool);
    m.def("add_logger", tir::pywowool::add_logger);
    m.def("unset_logger", tir::pywowool::unset_logger);

    py::register_exception<tir::pywowool::exception_t>(m, "TirException");
    py::register_exception<tir::pywowool::exception_json_t>(m, "TirJsonException");

    //------------------------------------------------------------------------------------------
    // Engine Object
    //------------------------------------------------------------------------------------------
    py::class_<eot::engine::Engine, tir::pywowool::engine_t>(m, "engine")
        .def(py::init([](py::dict const& kwargs) {
			eot::engine::Engine * engine = new eot::engine::Engine(tir::pywowool::convert_py_2_api_options(kwargs));
			return engine;
        }))
        .def("property", [](eot::engine::Engine const& self, std::string const& prop) {
            return eot::engine::get_engine_property(&self, prop.c_str());
        })
        .def("purge", [](eot::engine::Engine& self, std::string const& purge_descriptor) {
            return self.purge(purge_descriptor);
        })
        .def("info", [](eot::engine::Engine& self) {
            return self.info();
        })
        .def("languages", [](eot::engine::Engine& self) {
            return self.languages();
        })
        .def("release_domain", [](eot::engine::Engine& self, std::string const& domain_descriptor) {
            return self.release_domain(domain_descriptor);
        })
        .def("__getstate__", [](eot::engine::Engine const& self) {
            py::dict kwargs = tir::pywowool::convert_options_2_py(self.options);
            return kwargs;
        })
        .def("__setstate__", [](py::object self, py::dict kwargs) {
			// std::cout << "PLUGIN __setstate__ eot::engine::Engine(py::dict const& kwargs)" << std::endl;
            auto& p = self.cast<tir::pywowool::engine_t&>();
            new (&p) tir::pywowool::engine_t(kwargs);
        })
    ;

    //------------------------------------------------------------------------------------------
    // Language Identification
    //------------------------------------------------------------------------------------------
    py::class_<eot::language_identifier::LanguageIdentifier, tir::pywowool::lid_t>(m, "lid")
        .def(py::init([](tir::pywowool::engine_t const& eng, py::dict const& kwargs) {
            return new eot::language_identifier::LanguageIdentifier(eng, tir::pywowool::convert_py_2_api_options(kwargs));
        }))
        .def("language_identification_section", [](eot::language_identifier::LanguageIdentifier const& self, std::string const& doc) {
            return self.language_identification_section(doc);
        })
        .def("language_identification", [](eot::language_identifier::LanguageIdentifier const& self, std::string const& doc) {
            return self.language_identification(doc);
        })
		.def("__getstate__", [](eot::language_identifier::LanguageIdentifier const& self) {
            py::dict kwargs = tir::pywowool::convert_options_2_py(self.options);
            return kwargs;
        })
        .def("__setstate__", [](py::object self, py::dict kwargs) {
            auto& p = self.cast<tir::pywowool::lid_t&>();
            new (&p) tir::pywowool::lid_t(kwargs);
        })
    ;

    //------------------------------------------------------------------------------------------
    // Results object
    //------------------------------------------------------------------------------------------
    py::class_<eot::analyzer::Results, tir::pywowool::results_t>(m, "results")
        .def("to_json", [](eot::analyzer::Results const& self) {
            return self.to_json();
        })
        .def("metadata", [](eot::analyzer::Results const& self) {
            return self.metadata();
        })
        .def("internal_annotations", [](eot::analyzer::Results const& self) {
            return self.internal_annotations();
        })
        .def("language", [](eot::analyzer::Results const& self) {
            return self.language();
        })
        .def("id", [](eot::analyzer::Results const& self) {
            return self.id();
        })
		.def("get_concept" , [&](eot::analyzer::Results const& self, unsigned int begin_offset, unsigned int end_offset, std::string const & uri , bool unicode_offsets ) 
			-> std::variant<py::none, py::object>
		{
			plugin_Annotation * concept_internal_ptr = const_cast<eot::analyzer::Results &>(self).get_concept(begin_offset,end_offset,uri,unicode_offsets);
			return make_py_range(concept_internal_ptr);
		})
		.def("add_concept" , [&](eot::analyzer::Results const& self, unsigned int begin_offset, unsigned int end_offset, std::string const & uri , bool unicode_offsets )
			-> std::variant<py::none, py::object>
		{
    		plugin_Annotation * concept_internal_ptr = const_cast<eot::analyzer::Results &>(self).add_concept(begin_offset,end_offset,uri,unicode_offsets);
			return make_py_range(concept_internal_ptr);
		})
		.def("remove_pos" , [&](eot::analyzer::Results const& self, unsigned int begin_offset, unsigned int end_offset, std::string const & pos , bool unicode_offsets )
		{
    		const_cast<eot::analyzer::Results &>(self).remove_pos(begin_offset,end_offset,pos,unicode_offsets);
		})
		.def("get_byte_offset" , [&](eot::analyzer::Results const& self, unsigned int begin_offset)
		{
    		return  const_cast<eot::analyzer::Results &>(self).get_byte_offset(begin_offset);
		})

    ;

    using namespace pybind11::literals;

    //------------------------------------------------------------------------------------------
    // Domain Object
    //------------------------------------------------------------------------------------------
    py::class_<eot::domain::Domain, tir::pywowool::domain_t>(m, "domain")

        .def(py::init([](tir::pywowool::engine_t const& eng, std::string const filename, py::dict const& kwargs) {
			return new eot::domain::Domain(eng, filename, tir::pywowool::convert_py_2_api_options(kwargs));
        }))
        .def("info", [](eot::domain::Domain const& self) {
            return self.info();
        })
        .def("filename", [](eot::domain::Domain const& self) {
            return self.filename();
        })
        .def("process", [](eot::domain::Domain const& self, eot::analyzer::Results const& document) {
			if (lock_gil)
			{
				return self(document);
			}
			py::gil_scoped_release release; // Release the GIL
			return self(document);
        })
		.def("__getstate__", [](eot::domain::Domain const& self) {
            py::dict kwargs = tir::pywowool::convert_options_2_py(self.options);
            return kwargs;
        })
        .def("__setstate__", [](py::object self, py::dict kwargs) {
            assert(kwargs.find("name") != kwargs.end());
            auto& p = self.cast<tir::pywowool::domain_t&>();
            new (&p) tir::pywowool::domain_t(kwargs);
        })
    ;

    //------------------------------------------------------------------------------------------
    // Analyzer
    //------------------------------------------------------------------------------------------
    py::class_<eot::analyzer::Analyzer, tir::pywowool::analyzer_t>(m, "analyzer")
        .def(py::init([](tir::pywowool::engine_t const& eng, py::dict const& kwargs) {
            return new eot::analyzer::Analyzer(eng, tir::pywowool::convert_py_2_api_options(kwargs));
        }))
        .def("process", [](eot::analyzer::Analyzer const& self, std::string const& doc, py::dict const& kwargs) {
			auto options = tir::pywowool::convert_py_2_api_options(kwargs);
			if (lock_gil)
			{
				return self.process(doc, options).to_json();
			}
			return self.process(doc, options).to_json();
        },
            "Process a given input and return a JSON string."
            "\n\nEXAMPLE"
            "\n\twith wowool() as mc:"
            "\n\t\toptions['language']='english'"
            "\n\t\tresult_data = mc.process( input_text , options )",
            "doc"_a, "options"_a)
        .def("process_results", [](eot::analyzer::Analyzer const& self, std::string const& text, py::dict const& kwargs) {
			auto options = tir::pywowool::convert_py_2_api_options(kwargs);
			if (lock_gil)
			{
				return new eot::analyzer::Results(self.process(text, options));
			}
			py::gil_scoped_release release; // Release the GIL
			return new eot::analyzer::Results(self.process(text, options));
        },
            "Process a given input and return a JSON string."
            "\n\nEXAMPLE"
            "\n\twith wowool() as mc:"
            "\n\t\toptions['language']='english'"
            "\n\t\tresult_data = mc.process_results( input_text , options )",
            "doc"_a, "options"_a)        
        .def("process_document", [](eot::analyzer::Analyzer const& self, eot::analyzer::Results const text, py::dict const& kwargs) {
			if (lock_gil)
			{
            	return new eot::analyzer::Results(self.process_results(text));
			}
			// py::gil_scoped_release release; // Release the GIL
			return new eot::analyzer::Results(self.process_results(text));
        })
        .def("filename", [](eot::analyzer::Analyzer const& self) {
            return self.filename();
        })
        .def("__getstate__", [](eot::analyzer::Analyzer const& self) {
            py::dict kwargs = tir::pywowool::convert_options_2_py(self.options);
            return kwargs;
        })
        .def("__setstate__", [](py::object self, py::dict kwargs) {
            auto& p = self.cast<tir::pywowool::analyzer_t&>();

            new (&p) tir::pywowool::analyzer_t(tir::pywowool::get_default_engine(tir::pywowool::global_shared_engine_options) , kwargs);
        })
    ;

    //------------------------------------------------------------------------------------------
    // Filter object
    //------------------------------------------------------------------------------------------
    py::class_<eot::filter::Filter, tir::pywowool::filter_t>(m, "filter")
        .def(py::init([](eot::filter::FilterCollection const& filter_set) {
            return new eot::filter::Filter(filter_set);
        }))
        .def(py::init([](py::str filter_set) {
            return new eot::filter::Filter(filter_set);
        }))
        .def("process", [](eot::filter::Filter const& self, eot::analyzer::Results const& document) {
			return self(document);
        })
        .def("info", [](eot::filter::Filter const& self) {
            return self.info();
        })
        .def("__getstate__", [](eot::filter::Filter const& self) {
            py::str filter_set = tir::pywowool::convert_filterset(self);
            return filter_set;
        })
        .def("__setstate__", [](py::object self, py::str filter_set) {
            auto& p = self.cast<tir::pywowool::filter_t&>();
            new (&p) tir::pywowool::filter_t( filter_set );
        })
        ;
}
