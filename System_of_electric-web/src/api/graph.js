import service from './my-api'

export function get_graph(data) {
  return service.post('/graph', data)
}
