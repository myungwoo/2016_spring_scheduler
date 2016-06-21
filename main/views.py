from django.template import RequestContext
from django.shortcuts import render_to_response

from django.http import *

from django.contrib.auth.models import User
from main.models import Member, Schedule


def parse_time(stime):
	return int(stime.split(':')[0]) * 3600 + \
		int(stime.split(':')[1]) * 60 + \
		int(stime.split(':')[2])

def member_list(request):
	if request.method.lower() == 'post' and request.is_ajax():
		work = request.POST.get('work', '')
		if work == 'delete':
			id = int(request.POST.get('id', 0))
			member = Member.objects.get(id=id)
			member.delete()
			return HttpResponse('success')
		elif work == 'add':
			name = request.POST.get('name', '')
			phone_number = request.POST.get('phone_number', '')
			Member.objects.create(name=name, phone_number=phone_number)
			return HttpResponse('success')
	members = Member.objects.all().order_by('id')
	return render_to_response('member.html', RequestContext(request, {'members': members}))

def schedule_list(request):
	if request.method.lower() == 'post' and request.is_ajax():
		work = request.POST.get('work', '')
		if work == 'delete':
			id = int(request.POST.get('id', 0))
			schedule = Schedule.objects.get(id=id)
			schedule.delete()
			return HttpResponse('success')
		elif work == 'add':
			member_id = request.POST.get('member_id', 1)
			day = request.POST.get('day', 0)
			start_time = request.POST.get('start_time', 0)
			end_time = request.POST.get('end_time', 0)
			place = request.POST.get('place', '127.0318122,37.5899103')
			start_time = parse_time(start_time)
			end_time = parse_time(end_time)
			member = Member.objects.get(id=member_id)
			Schedule.objects.create(member=member, start_time=start_time, end_time=end_time, place=place)
			return HttpResponse('success')
	members = Member.objects.all().order_by('id')
	schedules = Schedule.objects.all().order_by('id')
	return render_to_response('schedule.html', RequestContext(request, {'members': members, 'schedules': schedules}))

def meeting_list(request):
	if request.method.lower() == 'post' and request.is_ajax():
		min_time = parse_time(request.POST.get('min_time', '00:00:00'))
		duration = int(request.POST.get('duration', 0))

		optimal = []
		members = Member.objects.all()
		for day in xrange(7):
			schedules = Schedule.objects.filter(week_day=day).order_by('end_time')
			optimal_absent_count = -1
			optimal_absent_set = set()
			optimal_start_time = 0
			for start_time in xrange(min_time, 86400-duration):
				absent = set()
				end_time = start_time + duration - 1
				member_place = {}
				for member in members:
					member_place[member.id] = [127.0318122, 37.5899103]
				for schedule in schedules:
					if schedule.end_time < start_time:
						member_place[schedule.member.id] = map(float, schedule.place.split(','))
					if schedule.start_time <= end_time and schedule.end_time >= start_time:
						absent.add(schedule.member)
				if optimal_absent_count == -1 or len(optimal_absent_set) > len(absent):
					optimal_absent_set = absent
					optimal_absent_count = len(absent)
					optimal_start_time = start_time
			if optimal_absent_count == -1:
				optimal.append({'found': False})
				continue
			try:
				places = []
				absent_id_set = set()
				for member in optimal_absent_set:
					absent_id_set.add(member.id)
				for member in members:
					if member.id in absent_id_set:
						continue
					places.append(member_place[member.id])
				x = (max(map(lambda x: x[0], places)) + min(map(lambda x: x[0], places))) / 2
				y = (max(map(lambda x: x[1], places)) + min(map(lambda x: x[1], places))) / 2
				place = ','.join(['%.7f'%x, '%.7f'%y])
			except:
				place = '127.0318122,37.5899103'
			optimal_absent = []
			for member in optimal_absent_set:
				optimal_absent.append({'name': member.name, 'phone_number': member.phone_number})

			start_time = '%02d:%02d:%02d' % (optimal_start_time / 3600, optimal_start_time % 3600 / 60, optimal_start_time % 60)
			optimal.append({'found': True, 'absent': optimal_absent, 'start_time': start_time, 'place': place})
		return JsonResponse({'optimal': optimal})

	return render_to_response('meeting.html', RequestContext(request, {}))



