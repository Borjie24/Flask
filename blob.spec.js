test('RecipeManager.vue: should fetch an image and set imageUrl', async () => {
  const mockBlob = new Blob(['image content'], { type: 'image/png' }); // Mock a Blob object
  const mockApi = new FetchAPI();
  mockApi.get.mockResolvedValue(mockBlob); // Mock the API response with a blob object

  const wrapper = shallowMount(RecipeManager);

  // Mock `URL.createObjectURL` to return a fake URL
  const mockCreateObjectURL = jest.spyOn(URL, 'createObjectURL').mockReturnValue('blob:http://localhost/image-url');

  await wrapper.vm.fetchImage();

  expect(mockApi.get).toHaveBeenCalledWith('/static/images/line_chart.png', { responseType: 'blob' });
  expect(wrapper.vm.imageUrl).toBe('blob:http://localhost/image-url');

  // Clean up the mock
  mockCreateObjectURL.mockRestore();
});
