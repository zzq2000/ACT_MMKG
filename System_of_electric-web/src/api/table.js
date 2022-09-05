import service from './my-api'

export function get_detection(data) {
  return service.post('/detection', data)
}
