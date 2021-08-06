# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline

class JpxgmnSpiderPipeline:
    def process_item(self, item, spider):
        return item

class ImagesDownloadPipeline(ImagesPipeline):
    # 自定义图片下载的Pipeline，也可以用上面那个默认的
    def file_path(self, request, response=None, info=None, *, item=None):
        # 重载图片处理管道 ImagesPipeline 的文件保存方法
        image_guid = request.url.split('/')[-1]
        return item['image_paths'] + '/' + image_guid   # 返回已修改的文件保存名称
