/**
 * App.tsx
 *
 * This module defines the main application component, which sets up the necessary providers and renders the Chat component.
 * It includes global CSS imports and initializes the React Query client.
 *
 */

import "./App.css";
import "@nlux/themes/nova.css";
import "react-toastify/dist/ReactToastify.css";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Chat } from "./Chat";

const queryClient = new QueryClient();

/**
 * The main application component.
 *
 * @returns {JSX.Element} The rendered application component.
 */
function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Chat />
    </QueryClientProvider>
  );
}

export default App;
