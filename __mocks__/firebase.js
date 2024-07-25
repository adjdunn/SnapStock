const firebaseMock = require('firebase-mock');
const mockauth = new firebaseMock.MockAuthentication();
const mockfirestore = new firebaseMock.MockFirestore();
const mocksdk = new firebaseMock.MockFirebaseSdk(
  (path) => {
    return path ? mockfirestore.child(path) : mockfirestore;
  },
  () => mockauth,
  () => null,
  () => null,
  () => null
);

jest.mock('firebase/app', () => mocksdk);
jest.mock('firebase/auth', () => mocksdk.auth());
