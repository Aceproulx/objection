export const evaluate = (js: string): void => {
  if (typeof Java !== 'undefined' && Java.perform) {
    Java.perform(() => { (0, eval)(js); });
  } else {
    (0, eval)(js);
  }
};
