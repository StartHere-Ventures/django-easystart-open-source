const path = require("path");
const BundleTracker = require("webpack-bundle-tracker");
const { VueLoaderPlugin } = require("vue-loader");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");

module.exports = {
  mode: "production",
  entry: ["regenerator-runtime/runtime.js", "./frontend/src/index.js"],
  output: {
    publicPath: "/static/dist/",
    filename: "[name]-[contenthash].js",
    chunkFilename: "[name]-[contenthash].js",
    path: path.resolve(__dirname, "static/dist/"),
  },
  resolve: {
    extensions: [".js", ".vue"],
    alias: {
      "@components": path.resolve(__dirname, "./frontend/src/Components"),
      "@utils": path.resolve(__dirname, "./frontend/src/utils"),
    },
  },
  plugins: [
    new VueLoaderPlugin(),
    new BundleTracker({ filename: "./webpack-stats.json" }),
    new CleanWebpackPlugin(),
    new MiniCssExtractPlugin({
      filename: "[name]-[contenthash].css",
    }),
  ],
  module: {
    rules: [
      {
        test: /\.m?js$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-env"],
            plugins: ["@babel/plugin-syntax-dynamic-import"],
          },
        },
      },
      {
        test: /\.vue$/,
        use: "vue-loader",
      },
      {
        test: /\.postcss$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
          },
          {
            loader: "css-loader",
            options: {
              importLoaders: 1,
            },
          },
          {
            loader: "postcss-loader",
          },
        ],
      },
    ],
  },
  optimization: {
    minimize: true,
    minimizer: [new CssMinimizerPlugin(), new TerserPlugin()],
  },
};
