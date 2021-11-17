<template>
    <div class="card-deck" v-for="i in Math.ceil(parseFloat(posts.length/4))" :key="i">
        <div class="card" v-for="x in 4" :key="x" :class="{'card-hidden': !posts[((i-1)*4)+x-1] }">
            <div v-if="posts[((i-1)*4)+x-1]">
                <router-link :to="`/post/${posts[((i-1)*4)+x-1].post_id}`">
                    <!-- <img :src="require(`/${posts[((i-1)*4)+x-1].title_image}`)" class="card-img-top" alt=""> -->
                    <img :src="`${posts[((i-1)*4)+x-1].title_image}`" class="card-img-top" alt="">
                    <div class="card-body">
                        <h5 class="card-title">{{removeHtml(posts[((i-1)*4)+x-1].title)}}</h5>
                        <p class="card-text card-content" v-text="removeHtml(posts[((i-1)*4)+x-1].content)"/>
                        <p class="card-text card-date"><small class="text-muted">{{$moment(posts[((i-1)*4)+x-1].create_date).fromNow()}}</small></p>
                    </div>
                    <div class="card-bottom">
                        <div class="card-writer">
                            <img :src="`${posts[((i-1)*4)+x-1].user_image}`" alt="postWriterImg">
                            <small>by {{posts[((i-1)*4)+x-1].nickname}}</small>
                        </div>
                        <div class="card-like">
                            <span class="material-icons">favorite</span>{{posts[((i-1)*4)+x-1].like_cnt}}
                        </div>
                    </div>
                </router-link>
            </div>
        </div>
    </div>
</template>

<script>
import common from '@/assets/js/common.js';

export default {
    name:"Card",
    mixins:[common],
    data() {
        return {
            cardDeckCnt:3,
            cardCnt:11,
        }
    },
    props:{
        posts:Array
    }
}
</script>

<style>

.card-deck{
  border-radius: 4px;
}
@media (min-width: 576px){
  .card-deck{
    padding-top: 80px;
  }
}
.card{
  border: 0 !important;;
  outline: 0;
}
.card a{
    /* anchor 태그 초기화 (Bootstrap때문에 important사용)*/
    color: inherit !important; /* 상위에서 사용한 fontcolor사용 */
    text-decoration: inherit !important; /* no underline */
}
.card-img-top{
    height: 230px;
}
.card-body{
    height: 205px;
    position: relative;
}
.card-title{
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.card-content{
    text-align: left;
    overflow: hidden;
    text-overflow: ellipsis;
    height: 100px;
}
.card-date{
    position: absolute;
    bottom:10px
}
.card-hidden{
    visibility: hidden;
}
.card-bottom{
  display: flex;
  justify-content: space-between; /** 요소가 일정한 간격을 두고 떨어짐, 2개 요소가 좌우로 최대한 멀어짐 */
  padding: 0.5rem;
  border-top: 1px solid rgb(248, 249, 250);
}
.card-writer{
    display: flex;
}
.card-writer > img {
  height: 1.5rem;
  widows: 1.5rem;
  display: block;
  border-radius: 50%;
  object-fit: cover;
  margin:0 0.5rem;
}
.card-like > span{
    position: relative;
    top: 2px;
    font-size: 1rem;
    padding-right: 0.5rem;
}
</style>