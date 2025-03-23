export default {
    testEnvironment: "jsdom",
    transform: {
        "^.+\\.tsx?$": "babel-jest"
    },
    moduleNameMapper: {
        "^@/(.*)$": "<rootDir>/src/$1",
        "^@components/(.*)$": "<rootDir>/src/components/$1",
        "^@constants/(.*)$": "<rootDir>/src/constants/$1",
        "^@styles/(.*)$": "<rootDir>/src/styles/$1"
    }
};
