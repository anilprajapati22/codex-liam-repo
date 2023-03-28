import { memo } from "react";

const Iframe = ({ classes='d-flex iframeclass-page2' }) => {
  console.log("child render");

  if ( classes === 'iframeclass-page1 lazyload'){
    return(
      <iframe src="https://my.spline.design/blob1copy-30869b055029cba7de507a93e958f784/" className={classes}  allowTransparency="true" background="transparent" allowFullScreen="" id='FrameID'></iframe>
    )

  }

  return (
    <> 
            <div class="col-lg-1 col-md-2 col-sm-3  col-3" >
            <iframe src="https://my.spline.design/blob1copy-30869b055029cba7de507a93e958f784/" className={classes}  allowTransparency="true" background="transparent" allowFullScreen="" id='FrameID'></iframe>
            </div>

    </>
  );
};

export default memo(Iframe);