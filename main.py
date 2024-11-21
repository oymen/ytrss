from bottle import default_app, static_file, route, response
from pytubefix import Playlist, YouTube
from feedgen.feed import FeedGenerator


@route("/")
def hello_world():
    return "<p>YouTube oynatma listelerini takip etmek için yazılmıştır.</p>"


@route("/favicon.ico")
def favicon():
    return static_file("favicon.ico", root="/home/oymen/yt-rss/static")


@route("/playlist/<listID>")
def playListToRSS(listID):
    p = Playlist("https://www.youtube.com/playlist?list=" + listID)

    fg = FeedGenerator()

    fg.id = p.playlist_id
    fg.title(p.title)
    fg.link(href=p.playlist_url, rel="alternate")
    fg.subtitle("Youtube oynatma listeleri için oluşturulmuştur.")
    fg.image(url="favicon.ico", width="16", height="16")

    # print(p.video_urls)

    for v in p.videos:
    # for i in p.video_urls[-1:-9:-1]:
        # v = YouTube(i)
        fe = fg.add_entry()
        fe.id(v.watch_url)
        fe.title(v.title)
        fe.link(href=v.watch_url + "&list=" + p.playlist_id)
        fe.published(v.publish_date)
        fe.description(
            f'<iframe width="560" height="315" src="{v.watch_url}"></iframe>'
        )

    response.content_type = "application/rss+xml; charset=UTF-8"
    return fg.rss_str(pretty=True)


application = default_app()

if __name__ == "__main__":
    application.run(debug=True, reloader=True)
