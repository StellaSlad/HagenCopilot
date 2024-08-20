/**
 * renderer.tsx
 *
 * This module defines a custom response renderer for displaying query responses.
 * It uses the ResponseRenderer type from the @nlux/react library to render the response content.
 * The renderer displays the main answer and, if available, the context information.
 *
 */

import { ResponseRenderer } from "@nlux/react";
import { QueryResponse } from "./types";

/**
 * Custom response renderer for displaying query responses.
 *
 * @param {QueryResponse} response - The response object containing the answer and context information.
 * @returns {JSX.Element} The rendered response content.
 */
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
