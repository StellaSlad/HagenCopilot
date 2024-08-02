import { AiChat, useAsBatchAdapter } from "@nlux/react";
import { personas } from "./personas";
import { QueryResponse } from "./types";
import { useRef, useState } from "react";
import { toast, ToastContainer } from "react-toastify";
import { useMutation } from "@tanstack/react-query";
import { renderer } from "./renderer";

const backendURL = "http://127.0.0.1:5000";

export const Chat = () => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [file, setFile] = useState<File | null>(null);

  const adapter = useAsBatchAdapter<QueryResponse>(async (message: string) => {
    try {
      const response = await fetch(backendURL + "/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ input: message }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: QueryResponse = await response.json();

      return data;
    } catch (error) {
      return {
        input: message,
        answer:
          "Entschuldigung, beim Verarbeiten Ihrer Anfrage ist ein Fehler aufgetreten. Prüfen Sie bitte Ihre VPN-Verbindung und versuchen Sie es erneut.",
      };
    }
  });

  const uploadDocumentMutation = useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData();
      formData.append("document", file);

      const response = await fetch(backendURL + "/upload_document", {
        method: "POST",
        body: formData,
      });

      if (response.status === 409) {
        throw new Error("Dokument bereits vorhanden.");
      }

      if (!response.ok) {
        throw new Error("Fehler beim Hochladen des Dokuments.");
      }

      return response.json();
    },
    onSuccess: () => {
      toast.success("Dokument erfolgreich hochgeladen!", {
        toastId: new Date().getTime(),
      });
    },
    onError: () => {
      toast.error("Dokument bereits vorhanden.", {
        toastId: new Date().getTime(),
      });
    },
  });

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files && files[0]) {
      setFile(files[0]);
    }
  };

  const handleClick = () => {
    if (!file) {
      return;
    }

    uploadDocumentMutation.mutate(file);
  };

  const triggerFileInput = () => {
    fileInputRef.current?.click();
  };

  return (
    <>
      <AiChat
        displayOptions={{ height: 600, width: 500, colorScheme: "dark"}}
        adapter={adapter}
        personaOptions={personas}
        messageOptions={
          {
            responseRenderer: renderer
          }
        }
      />
     <input
        type="file"
        ref={fileInputRef}
        accept=".pdf"
        onChange={handleFileChange}
        style={{ display: 'none' }}
      />
      <button onClick={triggerFileInput} style={{ margin: '8px' }} disabled={uploadDocumentMutation.isPending}>
        {uploadDocumentMutation.isPending ? "..." : "Dokument auswählen"}
      </button>

        <div style={{ margin: '8px' }}>
          <strong>Ausgewählte Datei:</strong> {file?.name || "Keine Datei ausgewählt"}
        </div>

      <button onClick={handleClick} style={{ margin: "8px" }} disabled={uploadDocumentMutation.isPending || !file}>
        {uploadDocumentMutation.isPending ? "Dokument wird hochgeladen..." : "Dokument hochladen"}
      </button>
      <ToastContainer theme={"dark"} position="bottom-right" />
    </>
  );
};
