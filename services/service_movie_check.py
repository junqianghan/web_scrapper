from services.service_base import ServiceBase
from urllib.request import urlopen
from bs4 import BeautifulSoup
from string import Template
import datetime
import os
import logging
import config
LOG = logging.getLogger(__name__)


class ServiceMovieCheck(ServiceBase):
    def __init__(self,**kwargs):
        super(ServiceMovieCheck, self).__init__(**kwargs)
        self.query_delay = self.conf_data["query_delay"]
        self.check_time = self.conf_data["check_time"]
        self.movies_file = "%s/%s" % (self.state_dir,
                                self.conf_data["movie_info_fn"])

    def _query_now(self):
        local_date_time = datetime.datetime.now()
        if int(local_date_time.hour) in self.check_time:
            return True
        else:
            return False

    def _get_movie_list(self):
        LOG.debug("get movie list")
        url = self.conf_data["index_url"]
        LOG.debug("check url %s" % url)
        html = urlopen(url).read().decode('gbk')

        bsObj = BeautifulSoup(html, 'lxml')
        head = bsObj.head
        cont = bsObj.find("div", {"class": "co_content8"})

        table = cont.findAll("tr")
        movieInfo = []
        for single in table:
            tdlist = single.findAll("td")
            if len(tdlist) < 2:
                continue;
            movieDict = {}
            movieName = tdlist[0].findAll("a")[1].get_text()
            movieUrl = tdlist[0].findAll("a")[1].attrs["href"]
            movieDate = tdlist[1].find("font").get_text()
            movieDict["Name"] = movieName
            movieDict["Date"] = movieDate
            movieDict["url"] = movieUrl
            movieInfo.append(movieDict)
            # print("%s %s" % (movieName,movieDate))
            # movieList.append(movieName)
            # dateList.append(movieDate)
            # print(movieDict)

        return movieInfo

    def _query_data(self):
        LOG.debug("query_data...")
        movie_info = self._get_movie_list()
        # print(movie_info)
        return movie_info

    def _check_new_data(self,cur_data):
        if not os.path.exists(self.movies_file):
            return cur_data

        pre_movies = config.get_json_file(self.movies_file,
                                          ["movies"])["movies"]
        new_movies = []
        for movie in cur_data:
            if movie["Name"] not in pre_movies:
                movie_dict = movie
                print(movie_dict)
                # movie_dict["Name"] = movie["Name"]
                # movie_dict["Date"] = movie["Date"]
                new_movies.append(movie_dict)
                # new_movie_list.append(movie)
                # new_date_list.append(date)

        return new_movies


    def _should_notify(self, new_data):
        if len(new_data)>0:
            LOG.info("%s new movies checked" % len(new_data))
            return True
        else:
            LOG.info("No new movies checked")
            return False

    def _get_mail_body(self, movies):
        body = ""
        i = 1
        for movie in movies:
            body += "<h3>%d. %s</h3>\n" % (i, movie["Name"])
            i += 1
            try:
                url = self.conf_data["base_url"] + movie["url"]
                print(url)
                html = urlopen(url).read().decode('gbk')
                bsObj = BeautifulSoup(html, 'lxml')
                cont = bsObj.find("div", {"id": "Zoom"})
                body += "%s\n" % cont
                movie["Body"] = cont
            except:
                LOG.error("ERROR %s" % movie)
                continue
        return body

    def _notify(self, new_data):
        LOG.info("Notify all recivers.")

        # tpl(template)
        tpl_fn = "etc/%s" % self.conf_data["email_template_fn"]
        with open(tpl_fn, encoding='utf-8') as f:
            mail_tpl = Template(f.read())

        local_time = "%s" % datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")
        body = self._get_mail_body(new_data)

        subject = self.conf_data["subject"] + "-%s" % datetime.date.today()
        receivers = self.conf_data["receivers"]
        contents = ""
        count = 1
        for movie in new_data:
            contents += "<tr><td>%d. </td><td>%s</td><td>%s</td></tr>" % \
                        (count, movie["Date"], movie["Name"])
            count += 1

        mail_str = mail_tpl.safe_substitute(TIME=local_time,
                                            CONTENT=contents,
                                            BODY=body,
                                            INDEX_URL=self.conf_data["index_url"])
        mail_info={
            "subject":subject,
            "receivers":receivers,
            "body":body,
            "bodyType":"html",
            "attachments":[]
        }
        self.mail_client.sendmail(mail_info)
        LOG.info("sendmail to %s" % (",".join(receivers)))

        print("notify")



    def _update_predata(self, cur_data=None):
        LOG.debug("update movie file..")
        self.pre_data = cur_data
        cur_movies = [item["Name"] for item in cur_data]
        cur_time = str(datetime.datetime.now())
        data_saving = {"movies":cur_movies,
                       "time":cur_time}
        config.save_json_file(self.movies_file, data_saving)

