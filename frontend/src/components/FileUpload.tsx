import React, { useState } from 'react';
import { UploadOutlined, WarningOutlined } from '@ant-design/icons';
import { Alert, Button, List, message, Spin, Typography, Upload } from 'antd';

const { Text } = Typography;

const FileUpload: React.FC = () => {
  const [fileList, setFileList] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any[]>([]);

  const uploadProps = {
    name: 'file',
    multiple: true,
    accept: '.mp3, .wav, .m4a, .ogg, .flac, .mp4, .mpeg, .mpga, .webm',
    beforeUpload: (file: any) => {
      const isDuplicate = fileList.some(item => item.name === file.name);
      if (isDuplicate) {
        message.error(`File with name ${file.name} already exists.`);
        return false;
      }
      setFileList(prevList => [...prevList, file]);
      return false; // Prevent automatic upload
    },
    onRemove: (file: any) => {
      setFileList(prevList => prevList.filter(item => item.uid !== file.uid));
    },
    fileList,
  };

  const handleTranscribe = async () => {
    if (fileList.length === 0) {
      message.warning('Please upload at least one file.');
      return;
    }

    setLoading(true);
    const formData = new FormData();
    fileList.forEach(file => {
      formData.append('files', file);
    });

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/transcribe`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setResults(data.results);
      message.success('Files transcribed successfully!');
    } catch (error) {
      message.error('Failed to transcribe files.');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFileList([]);
    setResults([]);
  };

  const renderContent = () => {
    if (loading) {
      return (
        <Spin tip="Transcribing...">
          <div style={{ height: '100px' }} />
        </Spin>
      );
    }

    if (results.length > 0) {
      return (
        <div>
          <List
            header={<div>Transcription Results</div>}
            bordered
            dataSource={results}
            renderItem={(item: any) => (
              <List.Item>
                {item.error ? (
                  <Alert
                    message={
                      <span>
                        <WarningOutlined style={{ marginRight: 8 }} />
                        <Text strong>{item.filename}</Text>: {item.error}
                      </span>
                    }
                    type="error"
                    showIcon
                  />
                ) : (
                  <div>
                    <Text strong>{item.filename}:</Text> {item.transcription}
                  </div>
                )}
              </List.Item>
            )}
          />
          <Button type="primary" onClick={handleReset} className="mt-2">
            Transcribe More
          </Button>
        </div>
      );
    }

    return (
      <>
        <p className="mb-2">
          Supports MP3, WAV, M4A, OGG, FLAC, MP4, MPEG, MPGA, and WEBM formats.
          <br />
          Maximum file size: 25MB.
          <br />
          Only English language is supported.
          <br />
          Up to 10 files can be uploaded at once and will overwrite existing files with the same
          name.
        </p>
        <Upload {...uploadProps}>
          <Button icon={<UploadOutlined />}>Upload Audio Files</Button>
        </Upload>
        <Button
          type="primary"
          onClick={handleTranscribe}
          disabled={fileList.length === 0}
          className="mt-2"
        >
          Transcribe
        </Button>
      </>
    );
  };

  return <div className="p-4">{renderContent()}</div>;
};

export default FileUpload;
