// frontend/webpack.config.js
const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const CopyWebpackPlugin = require("copy-webpack-plugin");
const TerserPlugin = require('terser-webpack-plugin');
const webpack = require('webpack');
const Dotenv = require('dotenv-webpack');

module.exports = (env = {}) => ({
  entry: env.entry || './src/index.tsx',
  output: {
    path: path.resolve(__dirname, "build"),
    filename: "static/js/main.js",
    publicPath: "",
    clean: true,
  },
  module: {
    rules: [
      { test: /\.tsx?$/, use: "ts-loader", exclude: /node_modules/ },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"],
      },
      {
        test: /\.svg$/,
        use: [
          {
            loader: '@svgr/webpack',
            options: { svgo: false }
          },
          {
            loader: 'url-loader',
            options: { limit: 8192, esModule: false }
          }
        ],
      },
      {
        test: /\.(png|jpg|jpeg|gif)$/i,
        type: 'asset/resource',
      },
    ],
  },
  resolve: {
    extensions: [".tsx", ".ts", ".js", ".jsx"],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: path.resolve(__dirname, "public", "index.html"),
      filename: "index.html",
      inject: true,
    }),
    new CopyWebpackPlugin({
      patterns: [
        {
          from: "public",
          filter: (filepath) => !filepath.endsWith("index.html"),
        },
      ],
    }),
    new Dotenv(),
  ],
  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          compress: {
            drop_console: true,
            drop_debugger: true
          }
        }
      })
    ],
    splitChunks: false,
    runtimeChunk: false,
  },
  mode: "production",
  devServer: {
    static: {
      directory: path.join(__dirname, 'public'),
    },
    port: 3001,
    historyApiFallback: true,
    hot: true,
    open: true,
  },
});
