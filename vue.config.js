module.exports = {
    configureWebpack: {
      devtool: 'source-map'
    },
    publicPath: process.env.BASE_URL//서브디렉토리명으로 배포 localhost:8081/jisuimon  , 배포시 BaseUrl
  }
  