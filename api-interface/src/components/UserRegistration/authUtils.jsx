// authUtils.js
export const parseJwt = (token) => {
    try {
      const [, payloadBase64] = token.split('.');
      const payloadJson = atob(payloadBase64);
      return JSON.parse(payloadJson);
    } catch (e) {
      return {};
    }
  };
  