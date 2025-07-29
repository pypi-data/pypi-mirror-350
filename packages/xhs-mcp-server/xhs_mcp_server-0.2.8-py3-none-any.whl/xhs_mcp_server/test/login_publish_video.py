from write_xiaohongshu import XiaohongshuPoster

poster = XiaohongshuPoster("/Users/luozhiling/")
test_json = {
"title": "生活的美好，在于每一步的前行",
    "content": "每个人的人生都是一场旅行，有时候我们会遇到困难和挑战，但只要我们勇敢地面对，就一定能找到属于自己的彩虹。",
    "images": [
      "/Users/luozhiling/Downloads/177b4d7a-63c0-4c2c-8ca1-8f5ca9eac7dd.mp4",
    ]
}
poster.login_to_publish_video(test_json["title"], test_json["content"], test_json["images"])