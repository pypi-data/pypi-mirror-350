from server import create_note

test_json = {
"title": "生活的美好，在于每一步的前行",
    "content": "每个人的人生都是一场旅行，有时候我们会遇到困难和挑战，但只要我们勇敢地面对，就一定能找到属于自己的彩虹。",
    "images": [
      "https://modelscope-studios.oss-cn-zhangjiakou.aliyuncs.com/aigc/text-to-image/c6f21407-61cf-467f-8750-17ded852290f_0.png",
      "https://modelscope-studios.oss-cn-zhangjiakou.aliyuncs.com/aigc/text-to-image/a86ee298-94a3-4be0-9cf0-3c6c757b002c_0.png",
      "https://modelscope-studios.oss-cn-zhangjiakou.aliyuncs.com/aigc/text-to-image/5a8289e8-224d-48b5-8416-9185c995a5a7_0.png",
      "https://modelscope-studios.oss-cn-zhangjiakou.aliyuncs.com/aigc/text-to-image/2b0be71a-0110-47b2-94a8-f89f3d87e7e0_0.png"
    ]
}

create_note(test_json["title"], test_json["content"], test_json["images"])