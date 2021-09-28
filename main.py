from flask import *
import requests
import json
import base64

app = Flask(__name__)

#escape
def esc_func(inp):
    inp = inp.replace("&","&amp;")
    inp = inp.replace("<","&lt;")
    inp = inp.replace(">","&gt;")
    return inp


#image to base64
def image_base64(url):
    if url == "":
        return ""
    
    response = requests.get(url, allow_redirects=False)
    if response.status_code != 200:
        e = Exception("HTTP status: " + response.status_code)
        raise e

    content_type = response.headers["content-type"]
    if 'image' not in content_type:
        e = Exception("Content-Type: " + content_type)
        raise e
    return base64.b64encode(response.content)


@app.route("/")
def home_page():
    return """
<html>
    <head>
        <meta charset="UTF-8">
    </head>

    <body>
        <p>jump to <a href="https://github.com/frozelab/github_profile_prompt">https://github.com/frozelab/github_profile_prompt</a></p>
    </body>
</html>
"""

@app.route("/<get_id>")
def main(get_id=None):
    login_name = ""
    bio = ""
    company = ""
    location = ""
    blog = ""

    avatar_url = ""
    avatar_base64 = ""
    
    res_json = requests.get("https://api.github.com/users/"+str(get_id))
    profile = json.loads(res_json.content.decode())

    if "name" in profile:
        if profile["name"] != None:
            login_name = str(profile["name"])
        elif "login" in profile:
            if profile["login"] != None:
                login_name = str(profile["login"])

    if "bio" in profile:
        if profile["bio"] != None:
            bio = esc_func(str(profile["bio"]))



    if "company" in profile:
        if profile["company"] != None:
            company = esc_func(str(profile["company"]))

    if "location" in profile:
        if profile["location"] != None:
            location = esc_func(str(profile["location"]))

    if "blog" in profile:
        if profile["blog"] != None:
            blog = esc_func(str(profile["blog"]))


    if "avatar_url" in profile:
        if profile["avatar_url"] != None:
            avatar_url = str(profile["avatar_url"])
            avatar_base64 = "data:image/png;base64,"+image_base64(avatar_url).decode()


    resp = make_response("""
<svg xmlns="http://www.w3.org/2000/svg" width="500" height="200">
  <rect x="1" y="0" width="500" height="200" rx="10" ry="10" fill="#000000" />
  <text class="tcolor" x="140" y="40" font-family="UTF-8" font-size="30">"""+login_name+"""</text>
  <text class="tcolor2" x="150" y="70" font-family="UTF-8" font-size="15">"""+bio+"""</text>

<filter id="colorMeGreen">
    <feColorMatrix in="SourceGraphic" type="matrix" values="0 0 0 0 0
                1 1 0 0 0
                0 0 0 0 0
                0 0 1 1 0" result="color"></feColorMatrix>

    <feGaussianBlur in="SourceGraphic" stdDeviation="5" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="color" />
      </feMerge>
  </filter>

  <image filter="url(#colorMeGreen)" href='"""+avatar_base64+"""' x="1" y="0" height="120" width="120"/>

  <text class="tcolor2" x="150" y="105" font-family="UTF-8" font-size="15">"""+company+"""</text>
  <image width="15" height="16" x="132" y="90" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAzCAYAAADVY1sUAAAAAXNSR0IArs4c6QAABP5JREFUaEPtmmtoHFUUx/93ZrLNzG52s02TKFbTfqhGjaUiWLUWRLQExbY0KIRaKNaWBrSJIgU/GMG2aLDB+ihobVJBW6IgCtIPNvXVVpRGrIXER8Vqiah026Q7yT5nZ47cCbGk2Zk7qTu7ScmB/XbPzPndc84995xZhitE2BXCgVmQ6eZJR4/EcoP0ZWa/bS8rouNylMU86Vrcp62fUrTkXTxsnqVOfS0GzZ8QYOVF3nxC0tKxMbQL96hrPcPkXXg6+wPtiK9BRKmy/VFcYUhSHEuU+7E5/Lrnl+dd+Ee2n17Um6DJFWCQissBIE0J1Ct3Ykt478wHuVG5G0+G35oFscMoX2iZlPMQYgwykyesIyJYMIW6PIQlNhbGPLR88YhBGVSyGhjIuhokMRmj1hAUFrDXWWTZOaaxCphw3ggJMgykwd/Dn+ELCH/JYO5HfFA9wuLmOXIOWgYVFVg3XItr5OtBIKRpFIvKlqIt2A2dzuc9/wiAykL4LL0PHyY7EZarbL2Ce0SCgtO5E/ioOuMp8ZpiQVqgNNggKdJRryxDa7hLqHs4tY8OJF5ApVwzPUFukO9CW6RbCHIotZd6Ejv8Bfkt9z0+rs4KjeF50RTTaIFyy38e4SHipR58nnqX3ku0+wfCICNmnsH2yGEMmX87JjvPJUlSsFNvRpU8HwAhS2lcLS9Cs/oc4tZZh1sCQWMR9OUO4lj6fWhSxJ9k56cO/3EY0XWFr5snzwc/cMeFw3AI9xsCQWVhBKVKewN8ObUuGuApsmxDJosX3Yt6PoMIa1rBFvgGYlkWMhgVhBbfUQZVCk/wimFlkENGqFsGDYqk+FfZiQDGgFvLGpGhpOuuz2GanbAhOWqvy1AKdVIDqpXrkCPDUTfA5uBn41skrThkSSl8jgTlChhkoJxpeDn6jZdAx5qYSguVxXamDJl/YWNwF5apTULdV/UN9KvRh4BU7h8I37HO6HGhMWN1ZLyyA8PmP2hWn8eK4GNC3U59Hf1unPQbJIDOaJ/QmPwg7VgR3CDULQqIxkLoiH4tNIaDXBpaLcHdWKquFOq+pj9Op4zj/niEt7r8JDLJwlyp1q7UbsKr+wUrhoA0do3nV/cAqeCHgFtPoiCAhDUMk5l2T8Jvvzcpy/FEoTtE3hzxfkEsbNLUxSTDtRcZfyaH4b3IWGM1isXKvdgcfkPoyXH9aTl8MMlEjjLYGu5BXVmDJ5hpCcI7Sx6mpmWgY+5RlEtBIYwnkFJU9jvKVqFSvgp92U+wrbL3/4OUprLzVne5PQ7aFl9NtWwhNoVfcYVx9ch0qOxJa4S2DC1BS2g3bitvdITxBFLqyn7GGKDt+iq8Gf0FsiTntdkjSOkr+1fpHtqfaMeeqlOXDzJdKvvO+KNUJ9+Mh0PPToIRnlqlqezOk8aW8/X0kNqKB7SWCbYLQXirW/zK7gzyaeptOpn9AlsjB6YOIr6aFHaFW6vbm+qmfuMIngq/M7NB+CBvwDg280F6U13UbxydBSlsEgie5p4jPnuET9+zlEK+D0IyU+zmyquUDIRDZKyxD5gRuWbCyJQf37p1DgPGEWj2zEt4kXWdoviaI2kridsDD2J9RYejlS9deIT+tPh3e1XomJJ5JGnqvNJipdbqCNI18gx9ZxyEyvgcwF1KCtKobsLq4NOOIHtG2uiEccj+zCaSWZBLd2iq/3zgoTXrkTxxdjmh9S9j+VVww5fyQQAAAABJRU5ErkJggg==" />
  <text class="tcolor2" x="150" y="125" font-family="UTF-8" font-size="15">"""+location+"""</text>
  <image width="15" height="16" x="132" y="112" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAeCAMAAAD5ENUgAAAABGdBTUEAALGPC/xhBQAAACBjSFJN AAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAABwlBMVEUAAACj/258+UHb/7d+ /z7a/7Z//zue/2md/2ly/i91/zJ1/jT///91/zT7//L///h0/jJ0/jNx/i54/zWS/1iS/1es/3Oz /3y3/4LB/5DA/44e/wAb/wDS/6dU/wBP/wDp/8nr/81c/wi0+5V98UZ38D528Dx07zl98Uaz+5SF 90918Dpx7zSF91CF/k108TmF/kyK/1J29Dqk/3t49D1x8DSj/3p98UZx7zVy7zZy7zVx7zV48D9x 7zRw7zR18Tl69EF39Dt69EF28Dxz8TeJ+1R28Dxx7zR58z528Dx07zlw7zN49D149Dx07zhx7zR5 8z548z528Dxz8TeI+1Nz8Td48D908Tl79EF79UJ78UNx7zVy7zZy7zZ78UOU/WN39DuU/WSF/0t0 9Da8/5J7/D5w8DOK/05z9DZz9DbL/6d7/D1w8DLK/6WK/09y8zRz8zXx/915+ztu8DBv8DB5+zvu /9qI/0xw8zJ6/Dxw8DJ6/DyP/1R29DiB/UVz8TaV/1539DuB/UZy8DaV/1529DmU/157+T9u7jGF /kx28DuG/k1x7zVw7zNy7zZw7zRy7zVx7zRx8DRv7zFv7jH///96JZQvAAAAjHRSTlMAAAAAAAAA AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM5kNH1OgMaiuUaJ7wnGLcDhv4DNuP57uSK/v21 US9QzrYW7PhR7fnvMjL5+VJSzbgYt4m4VDU76PrwPAWUBS3iAof+JtzdAX7+ASHX1wF1/f12ARzR bPttF8pk+hPDW/gPvA9T6hF6EZcPRykAAAABYktHRAyBs1FjAAAACXBIWXMAAAsRAAALEQF/ZF+R AAAAB3RJTUUH5QkZEzIDwEVCFwAAAYVJREFUKM9VkOcjglEUxk8k67VCWdmVvUmozIyQnRGy9x5l FCEZ9134g7333qLOp3N/57nnPOcAgCymrFyr0yO9TltRGSMDKWLlVdU1LEIcQmxNda08TmKKunqW RxwOxLP1DQqA+MamEKG0qTEBmltaCRIEgcDWljYwtPM4RcYOI8JFvtMAXSYpQ2ZLd0+vxYxTUxf0 kWL/QGJS4kA/+dIHVokJg0PJDDApQ4NSTzQMI1hvG02VXKWN2fBjnOrsE+mSLmPSjnVWmCL9pmeU mcqZ2VC/OTrXMb8w76Bz52BxSST+nMtO4k9cWoFV1xfdA9E9vlxrkLW+wXP/wW+sZwNsbm1H3GB7 a1NypdrZZf8Yu7ejwkfdPzgUw7LDgyOMQH18Ehayp8dqwuDs/IIKxcura4ogx+35Juzb484JMWBu brE54faOCSPIvfdiO8h7n/fHIN/3gDjhwVfwj0Dz6BeR6H/URDAofHoWn5+KIhEUvwR+Aq8lUQxK g2/B0mgEzPvHZ9jILz2auVh9fjO4AAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDIxLTA5LTI1VDE5OjUw OjAzKzA5OjAwTL/A9QAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyMS0wOS0yNVQxOTo1MDowMyswOTow MD3ieEkAAAAASUVORK5CYII="/>
  <text class="tcolor2" x="150" y="145" font-family="UTF-8" font-size="15">"""+blog+"""</text>
  <image width="15" height="16" x="132" y="130"  href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAAAXNSR0IArs4c6QAAA5VJREFUSEvtlktsE0cYx/8zu3bijR8bASkg8RC9oEDFAVFaWRFqBVJVLq1UxOtAlRAeqQQBURVuPfRSqiYpAYJyqBASp6hXVLUJIoCqSjwCASsXyEviESeB2Guc7HpnvmpNssRKnMTxcuuc7N2Z7zff9//2P8OwyNGcrKW0TOB4+DJKucYKDVPwgl7rIZ1PHUIaCXDiUODDwWAjNpV8XlCsgibfM/+kpuS30JXl8DF/NkkBG8P2AA4Hm7EtsG/B8RY88ULiCN3OtGGF8uEsVWWI2/2o9EXxQ7gNClfmjTvvhIyw6FTiE0xQCmW8HADlkZNhggwIKXBWv4WIWjFn7DlfPjQ7qMmoQZBH4GMlC+ofQTbGZBwHg7+iqnR33vh5X7QaJ+imeRXLlDVgmLcwMzY1LAax2fcF6iOXZ10842FSjFKzUYteuwsRZdmCssw3KSlGUaGsRX3od1Soa3JYOX9eZJ7ST8ZXEJSBxsNFQacWm5SGSeM4GbqCSn/U5bk/rqVbqDVVj7W+j8DBPYFODzJox/B14HvsD/6YZTIpJf1i7EUscxPlfDk4Uxel6Vw7dRqOQEjSMFbzjTgdaQP7ObGHXoonKGPlYIwhKUfBGfcM7hhMgELwsxJISIyTgTBbOrNdT736lGxY4EzxpNyvxHOcDv+B9f6t+ZvLlON0ZmwbJIRn4NfiJY4GW/Bx6c7FgR2d3rmW82UzEKRbFea05CxVcsB1wUvYUvpl4eAMWVjCV2Y1ejsIE/INNB7KPnM2IUjAoFEoTM2RqAgww7AYwFn9H6xQ1zFJkuKiDz3Wv/hM289saZHK/ey++Re1po4hwEM5jVkUeEj0olG/hwp1dbZccXuAuq0ObNeq3fI9MNvpYqoOQa57l7EDvqDHoE+eOGN2nGKZTkQDu1xwzLpF54waaDziVcZASr5GlX+3q59FExiRg1ilVsImCxwqkhRHt9WJEh7wLuO46MdveheWqCuzGY7Yz+iB1Y7t2gFGJIkxzh6ZnXQ+VYsyr0vdoN/FB5MnzJDdT4+s6zkad5l/U0vqO6817kODfmcauI+6revYodW4Gr8ncC8ulvcgoizNghJihB5bNxANfDOtuW7TOaMaGtdzfLiIzwlIyySi/l2uMzle7lzuVqkbkPV1KDBoBI8znZO3z3cmVRTYyXJcGq5FOvboOJTT0VPDuV+/7ejcS03R4MUeVf+DpyqXI8j7Oo9nOxb/A+0vMN0DTFuAAAAAAElFTkSuQmCC" />


  <style>
  .tcolor{
    fill: #00cc00;
    text-shadow: 0px 0px 7px #00cc00;
  }
  .tcolor2{
    fill: #00cc55;
    text-shadow: 0px 0px 7px #00cc55;
  }
  </style>
</svg>
""")
    resp.headers["Content-type"] = "image/svg+xml"
    return resp
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8000)
    pass
