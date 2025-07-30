declare module "*.svg" {
  import * as React from "react";
  export const ReactComponent: React.FunctionComponent<React.SVGProps<SVGSVGElement>>;
  const src: string;
  export default src;
}

interface Window {
  REACT_APP_API_URL?: string;
  REACT_APP_API_KEY?: string;
  Streamlit?: any;
}
