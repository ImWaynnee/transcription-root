import SearchTranscriptions from '@components/SearchTranscriptions';
import { fireEvent, render, screen, waitFor } from '@testing-library/react';

import '@testing-library/jest-dom';

import { mockFetch } from './utils/mock-fetch';

// Mock the matchMedia function for tests
beforeAll(() => {
  Object.defineProperty(window, 'matchMedia', {
    writable: true,
    value: jest.fn().mockImplementation(query => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: jest.fn(),
      removeListener: jest.fn(),
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
      dispatchEvent: jest.fn(),
    })),
  });
});

// Set up a mock fetch response before each test
beforeEach(() => {
  global.fetch = mockFetch({
    total_records: 1,
    current_page: 1,
    total_pages: 1,
    next_page: null,
    prev_page: null,
    results: [
      {
        id: 1,
        filename: 'test-sample-1',
        transcription:
          'My name is ethan. I was asked to come here by 11. Now it is already 3 p.m. They did not even serve me any food or drinks. Terrible.',
      },
    ],
  });
});

// Mock environment variables
jest.mock('@constants/environment', () => ({
  VITE_API_URL: 'http://localhost:8000',
}));

test('renders input and button', async () => {
  render(<SearchTranscriptions />);

  const inputElement = screen.getByPlaceholderText(/search by file name/i);
  const buttonElement = screen.getByRole('button', { name: /search/i });

  await waitFor(() => {
    expect(inputElement).toBeInTheDocument();
    expect(buttonElement).toBeInTheDocument();
  });
});

test('enables button when input is not empty', async () => {
  render(<SearchTranscriptions />);

  const inputElement = screen.getByPlaceholderText(/search by file name/i);
  const buttonElement = screen.getByRole('button', { name: /search/i });

  fireEvent.change(inputElement, { target: { value: 'test query' } });

  await waitFor(() => {
    expect(buttonElement).not.toBeDisabled();
  });
});

test('performs search and updates results', async () => {
  render(<SearchTranscriptions />);

  const inputElement = screen.getByPlaceholderText(/search by file name/i);
  const buttonElement = screen.getByRole('button', { name: /search/i });

  fireEvent.change(inputElement, { target: { value: 'sample' } });
  fireEvent.click(buttonElement);

  await waitFor(async () => {
    const results = await screen.findAllByText(/test-sample-1/i);
    expect(results.length).toBeGreaterThan(0);
  });
});

test('displays no results message when search returns nothing', async () => {
  // Mock fetch to return no results
  global.fetch = mockFetch({
    total_records: 0,
    current_page: 1,
    total_pages: 0,
    next_page: null,
    prev_page: null,
    results: [],
  });

  render(<SearchTranscriptions />);

  const inputElement = screen.getByPlaceholderText(/search by file name/i);
  const buttonElement = screen.getByRole('button', { name: /search/i });

  fireEvent.change(inputElement, { target: { value: 'asdfakgj' } });
  fireEvent.click(buttonElement);

  await waitFor(async () => {
    const noResultsMessages = await screen.findAllByText(/no data/i);
    expect(noResultsMessages.length).toBeGreaterThan(0);
  });
});
