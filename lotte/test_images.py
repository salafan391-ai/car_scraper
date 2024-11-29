from bs4 import BeautifulSoup as bs
html = '''
<ul class="swiper-wrapper" style="transition-duration: 0ms; transform: translate3d(-910px, 0px, 0px);"><li class="swiper-slide swiper-slide-duplicate swiper-slide-prev" data-swiper-slide-index="33" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017467.JPG">	
	</li> 
                               <li class="swiper-slide swiper-slide-active" data-swiper-slide-index="0" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017428.JPG">	
	</li>
                               <li class="swiper-slide swiper-slide-next" data-swiper-slide-index="1" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017421.JPG">	
	</li>
                               <li class="swiper-slide" data-swiper-slide-index="2" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017434.JPG">	
	</li>
                               <li class="swiper-slide" data-swiper-slide-index="3" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017433.JPG">	
	</li>
                               <li class="swiper-slide" data-swiper-slide-index="4" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017432.JPG">	
	</li>
                               <li class="swiper-slide" data-swiper-slide-index="5" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017427.JPG">	
	</li>
                               <li class="swiper-slide" data-swiper-slide-index="6" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017431.JPG">	
	</li>
                               <li class="swiper-slide" data-swiper-slide-index="7" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017430.JPG">	
	</li>                                 
                               <li class="swiper-slide" data-swiper-slide-index="8" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017429.JPG">	
	</li>
                               <li class="swiper-slide" data-swiper-slide-index="9" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017426.JPG">	
	</li>
                               <li class="swiper-slide" data-swiper-slide-index="10" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017425.JPG">	
	</li>
                               <li class="swiper-slide" data-swiper-slide-index="11" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017424.JPG">	
	</li>
                               <li class="swiper-slide" data-swiper-slide-index="12" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017440.JPG">	
	</li>
                               <li class="swiper-slide" data-swiper-slide-index="13" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017439.JPG">	
	</li>
                               <li class="swiper-slide" data-swiper-slide-index="14" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017438.JPG">	
	</li>
                               <li class="swiper-slide" data-swiper-slide-index="15" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017423.JPG">	
	</li>
                               <li class="swiper-slide" data-swiper-slide-index="16" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017437.JPG">	
	</li>
                               <li class="swiper-slide" data-swiper-slide-index="17" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017436.JPG">	
	</li>
                               <li class="swiper-slide" data-swiper-slide-index="18" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017422.JPG">	
	</li>
                               <li class="swiper-slide" data-swiper-slide-index="19" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017435.JPG">	
	</li>
                               <li class="swiper-slide" data-swiper-slide-index="20" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017441.JPG">	
	</li>
                               <li class="swiper-slide" data-swiper-slide-index="21" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017442.JPG">	
	</li>
                               <li class="swiper-slide" data-swiper-slide-index="22" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017443.JPG">	
	</li>
                               <li class="swiper-slide" data-swiper-slide-index="23" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017444.JPG">	
	</li>
                               <li class="swiper-slide" data-swiper-slide-index="24" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017445.JPG">	
	</li>
                               <li class="swiper-slide" data-swiper-slide-index="25" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017446.JPG">	
	</li>
                               <li class="swiper-slide" data-swiper-slide-index="26" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017447.JPG">	
	</li>
                               
		                       		<li class="swiper-slide" data-swiper-slide-index="27" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017461.JPG">	
	</li>
							   
		                       		<li class="swiper-slide" data-swiper-slide-index="28" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017462.JPG">	
	</li>
							   
		                       		<li class="swiper-slide" data-swiper-slide-index="29" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017463.JPG">	
	</li>
							   
		                       		<li class="swiper-slide" data-swiper-slide-index="30" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017464.JPG">	
	</li>
							   
		                       		<li class="swiper-slide" data-swiper-slide-index="31" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017465.JPG">	
	</li>
							   
		                       		<li class="swiper-slide" data-swiper-slide-index="32" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017466.JPG">	
	</li>
							   
		                       		<li class="swiper-slide swiper-slide-duplicate-prev" data-swiper-slide-index="33" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017467.JPG">	
	</li>
							                           
		                        
                           <li class="swiper-slide swiper-slide-duplicate swiper-slide-duplicate-active" data-swiper-slide-index="0" style="width: 910px;"><img width="910px" src="https://imgmk.lotteautoauction.net/AU_CAR_IMG_ORG_HP/202409/KS20240920017428.JPG">	
	</li></ul>
'''


soup = bs(html, 'html.parser')
images_ab = soup.find_all(class_='swiper-wrapper')
ab1 = []
for i in images_ab[0]:
    try:
        ab1.append(i.find('img').attrs['src'].split('/')[-1].split('.')[0][-2:])
    except AttributeError as attr:
        pass
print(ab1)
