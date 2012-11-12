#!/usr/bin/env python

#/*******************************************************************************
# Copyright (c) 2012 IBM Corp.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#/*******************************************************************************

'''
    Created on Jul 06, 2011

    Data transformation functions

    @author: Marcio A. Silva, Michael R. Hines
'''
from time import time, strftime, strptime, localtime
from datetime import datetime

from ..auxiliary.code_instrumentation import trace, cbdebug, cberr, cbwarn, cbinfo, cbcrit

class DataOpsException(Exception):
    '''
    TBD
    '''
    def __init__(self, msg, status):
        Exception.__init__(self)
        self.msg = msg
        self.status = status
    def __str__(self):
        return self.msg

@trace
def selective_dict_update(processid, maindict, extradict) :
    '''
    This function performs a "reverse" maindict.update(extradict) method, where
    the keys already present on maindict will not be overwritten by the values
    of the same keys on extradict
    '''
    try :
        _status = 100
        for _key,_value in extradict.iteritems() :
            if _key in maindict and maindict[_key] != "default":
                True
            else :
                maindict[_key] = _value
        _status = 0

    except Exception, e :
        _status = 23
        _fmsg = str(e)

    finally :
        if _status :
            _msg = "Selective update failure: " + _fmsg
            cberr(_msg)
            raise DataOpsException(_status, _msg)
        else :
            _msg = "Selective update success."
            cbdebug(_msg)
            return True 

@trace
def str2dic(input_string) :
    '''
    String needs to be in the form KEY1:VALUE1,KEY2:VALUE2,...,KEYN:VALUEN
    '''
    try :
        _status = 100
        _dictionary = {}
        for _kv_pair in input_string.split(',') :
            _kv_pair = _kv_pair.split(':')
            _dictionary[_kv_pair[0]] = _kv_pair[1]
        _status = 0

    except IndexError, msg:
        _status = 110
        _fmsg = "Input string was not properly formatted ("
        _fmsg += ':'.join(_kv_pair) + "): " + str(msg)
 
    except Exception, e :
        _status = 23
        _fmsg = str(e)

    finally :
        if _status :
            _msg = "String to dictionary conversion failure: " + _fmsg
            cberr(_msg)
            raise DataOpsException(_status, _msg)
        else :
            return _dictionary

@trace
def dic2str(input_dictionary) :
    '''
    String will be output in the form KEY1:VALUE1,KEY2:VALUE2,...,KEYN:VALUEN
    '''
    try :
        _status = 100
        _string = ''
        for _key,_value in input_dictionary.iteritems() :
            _string = str(_key) + ':' + str(_value) + ',' + _string
        _string = _string[0:-1]  
        _status = 0

    except Exception, e :
        _status = 23
        _fmsg = str(e)

    finally :
        if _status :
            _msg = "Dictionary to string conversion failure: " + _fmsg
            cberr(_msg)
            raise DataOpsException(_status, _msg)
        else :
            return _string

@trace
def wait_on_process(processid, proc_h, output_list) :
    '''
    TBD
    '''
    (output_stdout, output_stderr) = proc_h.communicate()
    
    if output_list is not None :
        if len(str(output_stdout)) > 0 :
            output_list.append(str(output_stdout))
        elif len(str(output_stdout) + str(output_stderr)) > 0 :
            output_list.append(str(output_stdout) + str(output_stderr))
    if proc_h.returncode > 1 :
        _msg = "There was an execution error: "
        _msg += str(output_stdout) + str(output_stderr)
        cberr(_msg)
        return False
    else :
        return True

@trace
def message_beautifier(processid, message) :
    '''
    TBD
    '''
    _new_message = ''
    if message.count("Usage") :
        _hide = True
        for _word in message.split() :
            if not _hide :
                _new_message += _word + ' '
            elif _word.count("Usage") :
                _new_message += _word + ' '
                _hide = False
            else :
                True
    else :
        _new_message = message
    
    _new_message = _new_message.replace("unknown object initialization failure:", '')
    return _new_message

def makeTimestamp(supplied_epoch_time = False) :
    '''
    TBD
    '''
    if not supplied_epoch_time :
        _now = datetime.now()
    else :
        _now = datetime.fromtimestamp(supplied_epoch_time)
        
    _date = _now.date()

    result = ("%02d" % _date.month) + "/" + ("%02d" % _date.day) + "/" + ("%04d" % _date.year)
        
    result += strftime(" %I:%M:%S %p", 
                        strptime(str(_now.hour) + ":" + str(_now.minute) + ":" + \
                                 str(_now.second), "%H:%M:%S"))
        
    result += strftime(" %Z", localtime(time())) 
    return result