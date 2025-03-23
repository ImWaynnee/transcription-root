export function mockFetch(data: any, ok: boolean = true) {
  return jest.fn().mockImplementation(() =>
    Promise.resolve({
      ok,
      json: () => Promise.resolve(data),
    })
  );
}
