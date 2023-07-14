 $(document).ready(function(){
	 $("#submit").click(function(){
		 const iFullName = $("#name").val();
		 const iCompanyName = $("#companyName").val();
		 const iPosition = $("#position").val();
		 const iSector = $("#sector").val();
		 const iPositionNow = $("#positionNow").val();
		 const iCompanyNow = $("#companyNow").val();
		 const iEducation = $("#education").val();
		 const iSkills = $("#skills").val();
		 const iExperience = $("#experience").val();
		 const iJobDescripton = $("#JobDescription").val();

		 const data = {
			 fullName: iFullName,
			 companyName: iCompanyName,
			 position: iPosition,
			 sector: iSector,
			 positionNow: iPositionNow,
			 companyNow: iCompanyNow,
			 education: iEducation,
			 skills: iSkills,
			 experience: iExperience,
			 JobDescription: iJobDescripton
		 }

		 $.ajax({
			 type: "POST",
			 url: "getJsonData",
			 data: JSON.stringify(data),
			 dataType: "json",
		 });
	 });
 });
