// @ts-check
"use strict";

const path = require("path");

/** @type {import('webpack').Configuration} */
const config = {
  target: "node",
  mode: "none",

  entry: "./src/extension.ts",

  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "extension.js",
    libraryTarget: "commonjs2",
  },

  externals: {
    // The vscode module is provided by the VS Code runtime
    vscode: "commonjs vscode",
  },

  resolve: {
    extensions: [".ts", ".js"],
  },

  module: {
    rules: [
      {
        test: /\.ts$/,
        exclude: /node_modules/,
        use: [
          {
            loader: "ts-loader",
          },
        ],
      },
    ],
  },

  devtool: "nosources-source-map",

  infrastructureLogging: {
    level: "log",
  },
};

module.exports = config;
