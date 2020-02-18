from aiohttp import web
import aiohttp_jinja2
import jinja2

@aiohttp_jinja2.template('index.html')
async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    # text = "Hello, " + name
    # return web.Response(text=text)
    return {'name': name}

app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('./template'))
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle)])
app.router.add_static('/static', path = './static', name = 'static')

if __name__ == '__main__':
    web.run_app(app)