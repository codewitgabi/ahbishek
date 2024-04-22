from django.shortcuts import render
from rest_framework import generics
from .models import Team, User, UserDocument, Document, StaffDocument
from .serializers import TeamSerializer, UserSerializer, UserDocumentUploadSerializer, StaffDocumentUploadSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.db import transaction


class TeamView(generics.ListCreateAPIView):
    serializer_class = TeamSerializer
    model = Team
    queryset = Team.objects.all()


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(["GET"])
def getUserDocuments(request):
	content_types = Document.objects.all()
	data = []
	
	for doc in content_types:
		json_data = {}
		model = doc.content_type.model
		
		if model == "userdocument":
			docID = doc.object_id
			
			user_doc = UserDocument.objects.get(id=docID)
			
			json_data["id"] = user_doc.id
			json_data["uploader"] = user_doc.uploader.username
			json_data["qualification_categories"] = user_doc.qualification_categories
			json_data["expiry_date"] = doc.expiry_date
			json_data["document"] = doc.document.url
			
			data.append(json_data)
	
	return Response(data)
	

class UserDocumentUploadView(generics.CreateAPIView):
	model = UserDocument
	queryset = UserDocument.objects.all()
	serializer_class = UserDocumentUploadSerializer
	
	@transaction.atomic
	def post(self, request):
		user = request.user
		doc = request.data.get("document")
		category = request.data.get("qualification_categories")
		exp_date = request.data.get("expiry_date")
		
		user_doc = UserDocument.objects.create(
			qualification_categories= category,
			uploader = user
		)
		user_doc.save()
		
		obj = Document.objects.create(
			content_object=user_doc,
			document=doc,
			expiry_date=exp_date
		)
		
		obj.save()
		
		return Response({
			"status": "success",
			"data": {
				"uploader": user_doc.uploader.username,
				"document": obj.document.url,
				"expiry_date": obj.expiry_date,
				"qualification_categories": user_doc.qualification_categories
			}
		})


class StaffDocumentUploadSerializer(generics.CreateAPIView):
	model = StaffDocument
	queryset = StaffDocument.objects.all()
	serializer_class = StaffDocumentUploadSerializer
	
	@transaction.atomic
	def post(self, request):
		staff_id = request.data.get("uploader")
		doc = request.data.get("document")
		category = request.data.get("client_categories")
		exp_date = request.data.get("expiry_date")
		
		staff_doc = StaffDocument.objects.create(
			client_categories= category,
			uploader_id = staff_id
		)
		staff_doc.save()
		
		obj = Document.objects.create(
			content_object=staff_doc,
			document=doc,
			expiry_date=exp_date
		)
		
		obj.save()
		
		return Response({
			"status": "success",
			"data": {
				"uploader": staff_doc.uploader.user.username,
				"document": obj.document.url,
				"expiry_date": obj.expiry_date,
				"client_categories": staff_doc.client_categories
			}
		})
		

@api_view(["GET"])
def getStaffDocuments(request):
	content_types = Document.objects.all()
	data = []
	
	for doc in content_types:
		json_data = {}
		model = doc.content_type.model
		
		if model == "staffdocument":
			docId = doc.object_id
			
			staff_doc = StaffDocument.objects.get(id=docId)
			
			json_data["id"] = staff_doc.id
			json_data["uploader"] = staff_doc.uploader.user.username
			json_data["client_categories"] = staff_doc.client_categories
			json_data["expiry_date"] = doc.expiry_date
			json_data["document"] = doc.document.url
			
			data.append(json_data)
	
	return Response(data)

