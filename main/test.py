import requests


if __name__ == '__main__':

    data = """<soapenv:Envelope xmlns:soapenv='http://schemas.xmlsoap.org/soap/envelope/' xmlns:clm='http://comarch.pl/loyalty/web/ws/clm'>
                                    <soapenv:Header/>
                                    <soapenv:Body>
                                    <clm:ProcessTransaction>
                                    <RequestData>
                                    <type>B</type>
                                    <partnerId>73</partnerId><locationCode>1</locationCode>
                                    <terminalCode>1</terminalCode>
                                    <transactionDate>170114163914</transactionDate>
                                    <receiptId>0001</receiptId>
                                    <online>true</online>
                                    <cardno>2999971300050</cardno>
                                    <amount>99</amount>
                                    <products>
                                    <item>
                                    <groupCode>1</groupCode>
                                    <code>1860</code>
                                    <quantity>1.000</quantity>
                                    <amount>100</amount>
                                    </item>
                                    </products>
                                    <pos_version>NQ</pos_version>
                                    <ip_cash_desk>127.0.0.1</ip_cash_desk>
                                    </RequestData>
                                    </clm:ProcessTransaction>
                                    </soapenv:Body>
                                    </soapenv:Envelope>"""

    url = 'http://185.98.81.132:8088/wscpstoclm/services/CLM'
    r = requests.post(url, data=data.encode('utf'), headers={'Content-Type': 'application/soap+xml; charset=utf-8', 'SOAPAction': 'ProcessTransaction'} )
    print(r.status_code)
