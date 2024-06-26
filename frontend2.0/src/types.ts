export interface DocumentMetadata {
  source: string;
  page: number;
  start_index: number;
  pk: number;
}

export interface DocumentContext {
  page_content: string;
  metadata: DocumentMetadata;
  type: string;
}

export interface QueryResponse {
  input: string;
  context?: DocumentContext[];
  answer: string;
}
