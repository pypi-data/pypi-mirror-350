from write_xiaohongshu import XiaohongshuPoster

poster = XiaohongshuPoster("/Users/luozhiling/")
test_json = {
"title": "生活的美好，在于每一步的前行",
    "content": "每个人的人生都是一场旅行，有时候我们会遇到困难和挑战，但只要我们勇敢地面对，就一定能找到属于自己的彩虹。",
    "images": [
      "/Users/luozhiling/Downloads/81d749c9-869a-4224-8470-66fbb7d7bd8e_0.png",
    ]
}
poster.login_to_publish(test_json["title"], test_json["content"], test_json["images"])