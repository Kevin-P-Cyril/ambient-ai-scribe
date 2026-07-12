import React, { useState } from "react";
import {
  Card,
  CardContent,
  Typography,
  Button,
  LinearProgress,
  Alert,
  Stack,
} from "@mui/material";

import { uploadAudio } from "../../api/api";

export default function AudioUploader({
  setTranscript,
  setSoap,
  setIcd,
}) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setMessage("");
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setMessage("Please select an audio file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      setLoading(true);
      setMessage("");

      const response = await uploadAudio(formData);

      const data = response.data;

      setTranscript(data.transcript);
      setSoap(data.soap);
      setIcd(data.icd_codes);

      setMessage("Audio processed successfully.");
    } catch (error) {
      console.error(error);

      setMessage(
        error.response?.data?.detail ||
          "Failed to process the audio."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card sx={{ mb: 2 }}>
      <CardContent>

        <Typography variant="h6" gutterBottom>
          Upload Consultation Audio
        </Typography>

        <Typography
          variant="body2"
          color="text.secondary"
          sx={{ mb: 2 }}
        >
          Supported formats:
          MP3, WAV, M4A
        </Typography>

        <Stack spacing={2}>

          <Button
            variant="outlined"
            component="label"
          >
            Choose Audio File

            <input
              hidden
              type="file"
              accept=".mp3,.wav,.m4a"
              onChange={handleFileChange}
            />
          </Button>

          {selectedFile && (
            <Typography>
              Selected:
              {" "}
              {selectedFile.name}
            </Typography>
          )}

          <Button
            variant="contained"
            onClick={handleUpload}
            disabled={loading}
          >
            Upload & Generate SOAP
          </Button>

          {loading && <LinearProgress />}

          {message && (
            <Alert severity={loading ? "info" : "success"}>
              {message}
            </Alert>
          )}

        </Stack>

      </CardContent>
    </Card>
  );
}