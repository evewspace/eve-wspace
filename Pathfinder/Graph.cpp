#include "Graph.h"

#define BOOST_PYTHON_STATIC_LIB
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

namespace Pathfinder
{

Graph::Graph()
:_nodeMap(_graph)
{}

Graph::NodeT Graph::findOrAddNode(const std::string &label)
{
	NodeT node = findNode(label);
	if(node == lemon::INVALID)
	{
		node = _graph.addNode();
		_systemMap.insert(SystemMapT::value_type(label, node));
		_nodeMap[node] = label;
	}

	return node;
}

Graph::NodeT Graph::findNode(const std::string &label)
{
	SystemMapT::iterator it = _systemMap.find(label);
	if(it == _systemMap.end())
	{
		return lemon::INVALID;
	} else {
		return it->second;
	}
}

void Graph::addEdge(const std::string &fromLabel, const std::string &toLabel)
{
	NodeT from = findOrAddNode(fromLabel);
	NodeT to = findOrAddNode(toLabel);
	_graph.addEdge(from, to);
}

LabelListT Graph::findPath(const std::string &fromLabel, const std::string &toLabel)
{
	LabelListT r;

	lemon::Bfs<lemon::ListGraph> bfs(_graph);
	NodeT from = findOrAddNode(fromLabel);
	NodeT to = findOrAddNode(toLabel);

	bfs.run(from);
	if(bfs.dist(to) > 0)
	{
		lemon::Path<GraphT> path = bfs.path(to);
		for(NodeT v = to;v != from; v = bfs.predNode(v))
		{
			r.push_back(_nodeMap[v]);
		}
		r.push_back(_nodeMap[from]);
	}

	return r;
}

BOOST_PYTHON_MODULE(Pathfinder)
{
	using namespace boost::python;

	class_<Pathfinder::LabelListT>("LabelListT")
		.def(vector_indexing_suite<LabelListT>());

	class_<Pathfinder::Graph, boost::noncopyable>("Graph")
		.def("addEdge", &Pathfinder::Graph::addEdge)
		.def("findPath", &Pathfinder::Graph::findPath)
	;
}

} // namespace Pathfinder