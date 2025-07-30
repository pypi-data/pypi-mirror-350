import mxupy as mu

from liveheroes.m.Models import *
from fastapi.responses import FileResponse

class VersionControl(mu.EntityXControl):

    class Meta:
        model_class = Version

    def download_app(self):
        """ 下载app

        Returns:
            FileResponse: apk 文件信息
        """
        # 获取最新版本
        im = self.get_one(order_by={'versionId': 'desc'})
        if im.check_data().error:
            return im
        lv = im.data
        
        apk_filename = lv.apk
        fn = mu.sys_file_dir() + '/' + apk_filename

        # 确保文件名在 HTTP 响应中正确设置
        # 用户看到的文件名，确保它以 .apk 结尾
        # 设置正确的 Content-Type 和 Content-Disposition 头部
        media_type="application/vnd.android.package-archive"
        headers={"Content-Disposition": f"attachment; filename={apk_filename}"}
        return FileResponse(fn, media_type=media_type, headers=headers)