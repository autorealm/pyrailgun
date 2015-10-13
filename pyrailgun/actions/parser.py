

__author__ = 'haku-mac'

import re
import types
from hashlib import md5
from bs4 import BeautifulSoup
from lxml import html

from pyrailgun.actions.action import RailGunAction

def xstrip(tag):
    dr = re.compile(r'<!--.*-->')
    tag = dr.sub('', tag)
    dr = re.compile(r'<br.*?>')
    tag = dr.sub('\n', tag)
    #dr = re.compile(r'<br />')
    #tag = dr.sub('\n', tag)
    dr = re.compile(r'<.*?>')
    tag = dr.sub('', tag)
    dr = re.compile('\r\n')
    tag = dr.sub('\n', tag)
    dr = re.compile('\n\n+')
    tag = dr.sub('\n\n', tag)
    return tag

class ParserAction(RailGunAction):

    def action(self, task_entry, shell_groups):
        rule = task_entry.get('rule')
        if None != rule:
            rule = rule.strip()
            self.logger.info("parsing with rule : " + rule)
        strip = task_entry.get('strip')
        match = task_entry.get('match')
        extract = task_entry.get('extract')
        if None != extract:
            extract = extract.strip()
        if None != match:
            match = match.strip()
            self.logger.info("parsing with match : " + match)
        datas = task_entry.get('datas')
        pos = task_entry.get('pos')
        attr = task_entry.get('attr')
        ignore = task_entry.get('ignore', 0)
        
        parsed_datas = []
        self.logger.info("start parser " + str(len(datas)))
        for data in datas:
            if (data == None or data == '') and not ignore:
                parsed_datas.append(None != extract and None or unicode(''))
                continue
            data = data.decode("utf-8")
            #self.logger.debug("parse from raw " + str(data))
            if None != rule:
                soup = BeautifulSoup(data)
                parsed_data_sps = soup.select(rule)
            elif None != match:
                parsed_data_sps = re.findall(match, data, re.M|re.I|re.L|re.U|re.S)
            if len(parsed_data_sps) == 0 and ignore:
                continue
            #else:
            #print 'rule find ' + str(len(parsed_data_sps))
            
            if None != pos:
                if pos > len(parsed_data_sps) - 1:
                    parsed_data_sps = []
                else:
                    parsed_data_sps = [parsed_data_sps[pos]]
            if len(parsed_data_sps) == 0 and not ignore:
                parsed_datas.append(None != extract and None or unicode(''))
            
            for tag in parsed_data_sps:
                if None != extract:
                    if None != rule:
                        _tags = tag.select(extract)
                    else:
                        _tags = html.fromstring(tag).xpath(extract)
                    tags = []
                    for tag in _tags:
                        if None != attr:
                            tag = tag.get(attr)
                        tag = unicode(tag)
                        if strip == 'true':
                            tag = xstrip(tag)
                        tag = tag.strip()
                        tags.append(tag)
                    parsed_datas.append(tags)
                else:
                    if None != attr:
                        #print tag
                        tag = tag.get(attr)
                        #attr_data = BeautifulSoup(tag.encode("utf8"))
                        #tag = attr_data.contents[0].get(attr)
                    tag = unicode(tag)
                    if strip == 'true':
                        tag = xstrip(tag)
                    tag = tag.strip()
                    #print type(tag)
                    parsed_datas.append(tag)
        self.logger.info("after parsing " + str(len(parsed_datas)))
        # set data to shell
        current_shell = self.get_current_shell(task_entry, shell_groups)
        if current_shell is not None and task_entry.get('setField') is not None and len(parsed_datas) > 0:
            field_name = task_entry.get('setField')
            #self.logger.debug("set " + field_name + " as " + str(parsed_datas))
            current_shell[field_name] = parsed_datas
        task_entry['datas'] = parsed_datas
        return task_entry
