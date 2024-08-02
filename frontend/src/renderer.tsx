import { ResponseRenderer } from "@nlux/react";

import { QueryResponse } from "./types";

export const renderer: ResponseRenderer<QueryResponse> = (response) => (
  <div className="response-container">
    <div className="answer">{response.content[0].answer}</div>
    {response.content[0].context && response.content[0].context.length > 0 && (
      <>
        <h4 style={{ paddingTop: "20px" }}>Kontext:</h4>
        <ul className="context-list">
          {response.content[0].context.map((ctx, index) => (
            <li key={index}>
              <div className="metadata">
                Name: {ctx.metadata.source}, Seite: {ctx.metadata.page}
              </div>
            </li>
          ))}
        </ul>
      </>
    )}
  </div>
);
