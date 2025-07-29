import os
import zipfile

from souJpg.comm import hdfsUtils


def updateVcgImageAI(vcgImageAIPath=None, hdfsPath=None):
    host = "gpu0.dev.yufei.com"
    port = 9000
    hdfsWraper = hdfsUtils.HdfsWraper(host=host, port=port)
    dst = "/tmp/vcgImageAI.zip"
    zf = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(vcgImageAIPath)
    for dirname, subdirs, files in os.walk(vcgImageAIPath):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            if "git" in absname:
                continue
            arcname = absname[len(abs_src) + 1 :]
            print("zipping %s as %s" % (os.path.join(dirname, filename), arcname))

            zf.write(absname, arcname)
    zf.close()
    hdfsWraper.upload(tmpFilePath=dst, hdfsFilePath=hdfsPath, deleteLocal=True)


if __name__ == "__main__":
    updateVcgImageAI(
        vcgImageAIPath="/data/projects/image-ai/",
        hdfsPath="hdfs://gpu0.dev.yufei.com:9000/data/zhaoyufei/imageAI_tf2.zip",
    )
