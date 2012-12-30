#ifndef _GRAPH_H
#define _GRAPH_H

#include <string>
#include <list>
#include <map>

#define LEMON_ONLY_TEMPLATES
#include <lemon/list_graph.h>
#include <lemon/bfs.h>

namespace Pathfinder
{

typedef std::vector<std::string> LabelListT;

class Graph
{
public:

	typedef lemon::ListGraph GraphT;
	typedef GraphT::Node NodeT;
	typedef GraphT::NodeMap<std::string> NodeMapT;
	typedef std::map<std::string, GraphT::Node> SystemMapT;

	Graph();

	void addEdge(const std::string &fromLabel, const std::string &toLabel);
	int edgeCount();
	int nodeCount();

	LabelListT findPath(const std::string &fromLabel, const std::string &toLabel);
	NodeT findNode(const std::string &label);
	

private:
	NodeT findOrAddNode(const std::string &label);

	GraphT _graph;
	NodeMapT _nodeMap;
	SystemMapT _systemMap;
};

} // namespace Pathfinder

#endif 
