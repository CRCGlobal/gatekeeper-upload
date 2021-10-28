import requests
import pymysql
conn = pymysql.connect(user="root", password="1qaz2wsx", host="127.0.0.1", port=3306, database="dotcam", autocommit=True, cursorclass=pymysql.cursors.DictCursor)
cur=conn.cursor()
cur.execute("SELECT id, datetime_capture, camera_id, path_full_image, path_crop_dot_number, path_crop_dot_text, candidate_number_1, candidate_number_2, candidate_number_3, candidate_number_4, candidate_number_5, candidate_conf_1, candidate_conf_2, candidate_conf_3, candidate_conf_4, candidate_conf_5, conf_txdot_text, conf_usdot_text, box_dot_number_left, box_dot_number_right, box_dot_number_top, box_dot_number_bottom, box_dot_text_left, box_dot_text_right, box_dot_text_top, box_dot_text_bottom FROM localscans WHERE datetime_sync IS NULL")
uplist=cur.fetchall()
for record in uplist:
	payload={'cameraid':record['camera_id'],'dotnum':record['candidate_number_1']}
	filename=record['path_full_image'].replace('tmp/images_dot_queue','results/images_truck')
	payload['candidate1'] = record['candidate_number_1']
	payload['candidate2'] = record['candidate_number_2']
	payload['candidate3'] = record['candidate_number_3']
	payload['candidate4'] = record['candidate_number_4']
	payload['candidate5'] = record['candidate_number_5']
	payload['confidence1'] = record['candidate_conf_1']
	payload['confidence2'] = record['candidate_conf_2']
	payload['confidence3'] = record['candidate_conf_3']
	payload['confidence4'] = record['candidate_conf_4']
	payload['confidence5'] = record['candidate_conf_5']
	try:
		uploadfile = {'imagefile': open(filename ,'rb')}
		print(record['id'])
		print(payload)
		response = requests.post('http://tc.crc.global/crcgatekeeper/api.php', data=payload, files=uploadfile)
		print(response)
		print(response.text)
		cur.execute("UPDATE localscans SET datetime_sync=now() WHERE id=%s AND datetime_sync IS NULL",(record['id'],))
	except Exception as e: print(e)
	input('go again?')
