import service from './my-api'

export function get_search(data) {
  return service.post('/search', data)
}
