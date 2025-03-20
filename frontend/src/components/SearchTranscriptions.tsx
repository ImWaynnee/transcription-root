import React, { useEffect, useState } from 'react';
import { ReloadOutlined } from '@ant-design/icons';
import { Button, Input, Pagination, Spin, Table, Typography } from 'antd';

const { Search } = Input;
const { Text } = Typography;

interface Transcription {
  id: number;
  filename: string;
  transcription: string;
}

const SearchTranscriptions: React.FC = () => {
  const [results, setResults] = useState<Transcription[]>([]);
  const [loading, setLoading] = useState(false);
  const [total, setTotal] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState('');
  const pageSize = 10;

  const fetchTranscriptions = (page: number, search: string = '') => {
    setLoading(true);
    const endpoint = search
      ? `/search?filename=${search}&page=${page}&limit=${pageSize}`
      : `/transcriptions?page=${page}&limit=${pageSize}`;

    fetch(`${import.meta.env.VITE_API_URL}${endpoint}`)
      .then(response => response.json())
      .then(data => {
        setResults(data.results);
        setTotal(data.total_records);
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchTranscriptions(currentPage, searchTerm);
  }, [currentPage, searchTerm]);

  const onSearch = (value: string) => {
    setSearchTerm(value);
    setCurrentPage(1); // Reset to first page on new search
  };

  const onRefresh = () => {
    fetchTranscriptions(currentPage, searchTerm);
  };

  const columns = [
    {
      title: 'File Name',
      dataIndex: 'filename',
      key: 'filename',
      render: (text: string) => (
        <div className="w-[70px]">
          <Text strong>{text}</Text>
        </div>
      ),
    },
    {
      title: 'Transcription',
      dataIndex: 'transcription',
      key: 'transcription',
      width: '90%',
    },
  ];

  return (
    <div className="p-4">
      <div className="flex flex-row gap-x-4 w-full">
        <Search
          className="w-full"
          placeholder="Search by file name"
          enterButton="Search"
          onSearch={onSearch}
        />
        <Button icon={<ReloadOutlined />} onClick={onRefresh}>
          Refresh
        </Button>
      </div>
      <Spin spinning={loading} tip="Loading...">
        <Table
          className="mt-4"
          columns={columns}
          dataSource={results}
          pagination={false}
          rowKey="id"
        />
      </Spin>
      <Pagination
        current={currentPage}
        total={total}
        pageSize={pageSize}
        onChange={page => setCurrentPage(page)}
        className="!mt-4"
      />
    </div>
  );
};

export default SearchTranscriptions;
