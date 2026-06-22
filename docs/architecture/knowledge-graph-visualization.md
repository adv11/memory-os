# Knowledge Graph Visualization Design

## Goal

Help users visually explore what they are learning and how concepts relate to topics and sessions.

## V1 Data Model

The graph is generated from relational data:

- Topic node
- Learning session node
- Concept node

Edges:

- Topic contains learning session.
- Learning session includes concept.

## V1 Graph API

`GET /api/v1/graph?range=LAST_30_DAYS`

The backend returns a frontend-ready graph projection:

```json
{
  "nodes": [],
  "edges": []
}
```

## Time Filters

- Today
- Last 7 Days
- Last 30 Days
- Last 3 Months
- Last 6 Months
- Last Year
- All Time

## Frontend Renderer

Use React Flow because it is production-ready, flexible, and works well with React and Next.js.

Required interactions:

- Zoom
- Pan
- Fit view
- Click node
- Filter by date range

## Node Types

- Topic: highest-level node, visually prominent.
- Session: medium node, includes date and difficulty.
- Concept: compact node.

## Future Extensions

Do not implement these in V1:

- AI-generated semantic edges.
- Knowledge decay coloring.
- Revision priority overlays.
- Graph database persistence.

