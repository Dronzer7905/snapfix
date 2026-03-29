module.exports = {
  root: true,
  parser: "@typescript-eslint/parser",
  parserOptions: {
    ecmaVersion: 2020,
    sourceType: "module",
  },
  plugins: ["@typescript-eslint"],
  extends: [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
  ],
  rules: {
    // Require typed alternatives to bare `any`
    "@typescript-eslint/no-explicit-any": "error",
    // Enforce consistent code style
    "@typescript-eslint/explicit-function-return-type": [
      "warn",
      { allowExpressions: true },
    ],
    // Prevent floating promises in async code
    "@typescript-eslint/no-floating-promises": "error",
    // Prefer `unknown` over `any` for catch bindings
    "@typescript-eslint/use-unknown-in-catch-callback-variable": "off",
    // Allow `_` prefix for intentionally unused vars
    "@typescript-eslint/no-unused-vars": [
      "warn",
      { argsIgnorePattern: "^_", varsIgnorePattern: "^_" },
    ],
    "no-console": "warn",
  },
  env: {
    node: true,
    es2020: true,
  },
  ignorePatterns: ["dist/**", "out/**", "node_modules/**", "*.js"],
};
