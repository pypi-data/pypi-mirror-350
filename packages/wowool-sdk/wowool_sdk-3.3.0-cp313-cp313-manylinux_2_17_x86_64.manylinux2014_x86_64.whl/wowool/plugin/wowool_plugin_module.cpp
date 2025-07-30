// ----------------------------------------------------------------------------------
// Copyright (c) 2020 EyeOnText, All Rights Reserved.
// NOTICE:  All information contained herein is, and remains the property of EyeOnText.
// ----------------------------------------------------------------------------------
#define WITH_THREAD

//#define TIR_DESCRIPTOR

#ifdef TIR_DESCRIPTOR
	#include "eot/analyzer/analyzer.hpp"
	#include "eot/analyzer/options.hpp"
	#include "eot/analyzer/tir.hpp"
#endif

#include "eot/common/Exception.hpp"
#include "eot/common/c/plugin.h"
#include "eot/common/options.hpp"
#include "eot/domain/domain.hpp"

#include <codecvt>
#include <functional>
#include <iostream>
#include <mutex>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>
#include <regex>
#include <set>
#include <string>
#include <thread>
#include "nlohmann/json.hpp"
#include "plugins/API.hpp"
#include "wowool_plugin.hpp"

namespace py = pybind11;
using namespace tir::wowool;

py::object python_object_range_obj;

////////////////////////////////////////////////////////////
typedef std::vector<wow::python::AttributesPair> python_object_attributes_type;
typedef wow::python::python_object_range python_object_range;
using wow::python::AttributesPair;
using wow::python::python_object_attributes;
using wow::python::python_object_match_context;
using wow::python::python_token;

PYBIND11_MAKE_OPAQUE(python_object_attributes_type);

#ifdef TIR_DESCRIPTOR

static eot::common::Options global_shared_engine_options = {
	{std::string("language"), std::string("auto")},
	{std::string("dummy"), std::string("true")},
	{std::string("pytryoshka"), std::string("true")}};

eot::analyzer::Engine engine(global_shared_engine_options);

struct Descriptor
{
	eot::analyzer::Analyzer analyzer;
	eot::domain::Domain domain;
	Descriptor(std::string const &language, std::string const &pipline_descriptor)
	{
		eot::common::Options analyzer_options = {
			{std::string("language"), std::string(language)},
			{std::string("pytryoshka"), std::string("true")}};
		analyzer = eot::analyzer::Analyzer(engine, analyzer_options);
		domain = eot::domain::Domain(engine, pipline_descriptor);
	}

	std::string process(std::string const &data)
	{
		eot::common::Options const options;
		auto document = analyzer.process(data, options);
		document = domain(document);
		return document.to_json();
	}
};

// cache for the analyzers.
typedef std::map<std::string, Descriptor> Name2Descriptor;
Name2Descriptor descriptors;

// process a given domains.
std::string process(std::string const &language, std::string const &pipline_descriptor, std::string const &data)
{
	std::string id = language + pipline_descriptor;
	{
		Name2Descriptor::const_iterator it = descriptors.find(id);
		if (it == descriptors.end())
		{
			descriptors.emplace(id, Descriptor(language, pipline_descriptor));
		}
	}
	{
		Name2Descriptor::iterator it = descriptors.find(id);
		if (it != descriptors.end())
		{
			return it->second.process(data);
		}
		else
		{
			assert(false);
		}
	}
	return "";
}
#else
std::string process_donotuse(std::string const &language, std::string const &pipline_descriptor, std::string const &data)
{
	return "is deprecated check wowool_plugin";
}
#endif

void __init__callback(py::module &module)
{
}
auto __exit__callback = []() {};

// ----------------------------------------------------------------------------
// Python Bindings for the wowool_plugin.
// ----------------------------------------------------------------------------
PYBIND11_MODULE(_wowool_plugin, m)
{
	using namespace pybind11::literals;

	__init__callback(m);
	m.add_object("_cleanup", py::capsule(__exit__callback));

	py::class_<python_token>(m, "python_token")
		.def("has_property", &python_token::has_property)
		.def("head", &python_token::head)
		.def("pos", &python_token::pos, py::arg("idx") = 0)
		.def("stem", &python_token::stem, py::arg("idx") = 0)
		.def("__repr__", &python_token::str, "Returns literal")
		.def("__str__", &python_token::str, "Returns literal");

	py::class_<python_object_range>(m, "annotation_range", "\nA annotation range marks the begin and "
														   "end of a annotation collection.")
		.def(py::init([](plugin_Annotation *cnpt) {
			return new python_object_range(cnpt);
		})) // C++ constructor, shadowed by raw ctor
		.def_property_readonly("tokens", &python_object_range::tokens, "Returns a list with the tokens of this range.")
		.def("literal", &python_object_range::literal, "\n:param separator: separator between the tokens, default space."
													   "\n:type separator: str"
													   ":returns: a literal string of this range, you can specify the "
													   "literal delimiter ",
			 py::arg("separator") = " ")
		.def("canonical", &python_object_range::canonical, "\n:param separator: separator between the tokens, default space."
														   "\n:type separator: str"
														   ":returns: a canonical string of this range, you can specify the "
														   "canonical delimiter ",
			 py::arg("separator") = " ")
		.def("__repr__", &python_object_range::repr, ":returns: the literal string of this range, you can specify the "
													 "stem delimiter.")
		.def("__str__", &python_object_range::str, ":returns: the literal string of this range, you can specify the "
												   "stem delimiter.")
		.def("stem", &python_object_range::stem, "\n:param separator: separator between the tokens, default space."
												 "\n:type separator: str"
												 ":returns: a string with the stems of this range, you can specify "
												 "the literal delimiter ",
			 py::arg("separator") = " ")
		.def("find", &python_object_range::find, "\n:param uri: uri of a concept to find."
												 "\n:type uri: str"
												 "\n:returns: a list of annotation_range object"
												 "\n:type: list(annotation_range)",
			 py::arg("uri"))
		.def("find_one", &python_object_range::find_one, "\n:param uri: uri of a concept to find."
														 "\n:type uri: str"
														 "\n:returns: a annotation_range object"
														 "\n:type: annotation_range",
			 py::arg("uri"))
		// when accessing the scope using a . then the return will be one range.
		// example capture.person will return the first person.
		// .def("__getattr__", &python_object_range::get_attr )
		.def(
			"__getattr__",
			static_cast<py::object (python_object_range::*)(std::string const &)>(
				&python_object_range::get_attr))
		// when accessing the scope using a ['person'] then the return will be  a
		// vector of ranges example capture['person'] will return the all the
		// persons in the scope.
		.def("__getitem__", static_cast<std::vector<python_object_range> (python_object_range::*)(std::string const &)>(&python_object_range::get_item))
		.def("__getitem__", static_cast<std::vector<python_object_range> (python_object_range::*)(py::tuple const &)>(&python_object_range::get_item))
		.def("attributes", &python_object_range::attributes, "Returns the Attribute Object of this range.")
		.def("has", &python_object_range::has, "\n:param name: name of the attribute."
											   "\n:type name: str"
											   "\n:returns: true if this range has the given attribute."
											   "\n:type: bool",
			 py::arg("name"))
		.def("attribute", &python_object_range::get_attribute, "\n:param name: name of the attribute."
															   "\n:type name: str"
															   "\n:returns: the value of the given attribute."
															   "\n:type: str",
			 py::arg("name"))
		.def("add_attribute", &python_object_range::add_attribute, "Add a attribute to this range", py::arg("key"), py::arg("value"))
		.def("add_concept", &python_object_range::add_concept, "Add a concept ( semantic annotation ) over this range."
															   "\n"
															   "\n    ::"
															   "\n"
															   "\n      capture = match.capture()"
															   "\n      capture.add_concept('other_uri')"
															   "\n",
			 py::arg("uri"))
		.def("uri", &python_object_range::get_uri, "\n:returns: the uri of this annotation"
												   "\n:type: str")
		.def("begin_offset", &python_object_range::get_begin_offset, "\n:returns: a int with the begin offset of this range."
																	 "\n:type begin_offset: int")
		.def("end_offset", &python_object_range::get_end_offset, "\n:returns: a int with the end offset of this range."
																 "\n:type end_offset: int")
		.def("remove", &python_object_range::remove_concept, "remove the annotation over this range.")
		.def("__bool__", &python_object_range::pybool);

	py::class_<python_object_match_context>(
		m, "match_info", "\nIs all the data related to the match of the triggered function."
						 "\nThis object contains the capture, rule and the sentence where the "
						 "match was located."
						 "\n\nEXAMPLE"
						 "\n match = wowool_plugin.match_info()"
						 "\n capture_group = match.capture()")
		.def(py::init([]() { return new python_object_match_context(); }))
		.def("uri", &python_object_match_context::to_string, ":returns: the uro of the rule")
		.def("sentence", &python_object_match_context::sentence, "The sentence object (range) where the match has occurred.")
		.def("rule", &python_object_match_context::rule, ":returns: the annotation range that the rule has matched. "
														 "\n"
														 "\n    ::"
														 "\n"
														 "\n      ex rule: { <'Mr'> { <'Fawlty'> }= "
														 "::python::module_name::silly_person }= rule_context;"
														 "\n"
														 "\nHere the range is 'Mr Fawlty'= rule_context."
														 "\n:type: annotation_range")
		.def("capture", &python_object_match_context::capture, ":returns: the annotation range that we have captured. "
															   "\n"
															   "\n    ::"
															   "\n"
															   "\n        ex rule: { <'Mr'> { <'Fawlty'> }= "
															   "::python::module_name::silly_person }= rule_context;"
															   "\n"
															   "\nHere the range is 'Fawlty'= silly_person."
															   "\n:type: annotation_range")
		.def("property", &python_object_match_context::property, ":returns: a property of the range (ex: language)", py::arg("key"))
		.def("range", &python_object_match_context::make_range, "\n:param begin_range: begin position of the range."
																"\n:type begin_range: annotation_range"
																"\n:param end_range: end position of the range."
																"\n:type end_range: annotation_range"
																"\n:returns: a annotation range for the given begin and end "
																"annotation."
																"\n:type: annotation_range",
			 py::arg("begin_range"),
			 py::arg("end_range"));

	// py::bind_vector<python_object_attributes>(m, "python_object_attributes");

	py::class_<python_object_attributes>(m, "Attributes")
		.def("has", &python_object_attributes::has)
		.def("__len__", &python_object_attributes::size)
		.def(
			"__iter__",
			[](python_object_attributes &v) {
				return py::make_iterator(v.begin(), v.end());
			},
			py::keep_alive<0, 1>()) /*Keep vector alive while iterator is used*/
		.def("__bool__", &python_object_attributes::pybool)
		.def("__repr__", &python_object_attributes::to_string)
		.def("__str__", &python_object_attributes::to_string);

	py::class_<AttributesPair>(m, "attributes_vp")
		.def("name", &AttributesPair::name)
		.def("value", &AttributesPair::value)
		.def("__repr__", &AttributesPair::to_string)
		.def("__str__", &AttributesPair::to_string);

#if TIR_DESCRIPTOR
	m.def("process", process);
#endif
}
