import React from 'react';
import FileUpload from '@components/FileUpload';
import SearchTranscriptions from '@components/SearchTranscriptions';
import { Tabs } from 'antd';

const App: React.FC = () => {
  const items = [
    {
      key: '1',
      label: 'Transcribe Audio Files',
      children: <FileUpload />,
    },
    {
      key: '2',
      label: 'View Past Transcriptions',
      children: (
        <>
          <SearchTranscriptions />
        </>
      ),
    },
  ];

  return (
    <div className="container mx-auto">
      <h1 className="text-2xl font-bold text-center my-4">Transcribe Audio to Text</h1>
      <Tabs defaultActiveKey="1" centered items={items} />
    </div>
  );
};

export default App;
