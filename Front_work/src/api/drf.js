const SERVER_URL = process.env.VUE_APP_SERVER_URL
export default {
  URL: SERVER_URL,
  ROUTES: {
    signup: '/api/v2/signup/',
    login: '/api/v2/api-token-auth/',
  }
}