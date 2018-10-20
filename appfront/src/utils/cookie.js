import Cookie from 'js-cookie'
export function getCookie (key) {
  let value = Cookie.get(key);
  return value;
}
export function setCookie (key, value, time) {
  Cookie.set(key, value, time);
}
export function clearCookie(key) {
  Cookie.set(key, '', -1);
}
