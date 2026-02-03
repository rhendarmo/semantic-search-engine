export type SearchResult = {
  doc_id: string;
  movie_id: number;
  title: string;
  year: number | null;
  genres: string[];
  rating: number | null;
  vote_count: number | null;
  overview: string;
  score: number;
};

export type SearchResponse = {
  query: string;
  top_k: number;
  model_name: string;
  num_docs: number;
  results: SearchResult[];
};
