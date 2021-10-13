<template>
<div class="card-deck" v-for="i in Math.ceil(parseFloat(posts.length/4))" :key="i">
    <div class="card" v-for="x in 4" :key="x" :class="{'card-hidden': !posts[((i-1)*4)+x-1] }">
        <div v-if="posts[((i-1)*4)+x-1]">
            <img :src="require(`@/${posts[((i-1)*4)+x-1].postImage}`)" class="card-img-top" alt="">
            <div class="card-body">
                <h5 class="card-title">{{posts[((i-1)*4)+x-1].title}}</h5>
                <p class="card-text card-content">{{posts[((i-1)*4)+x-1].content}}</p>
                <p class="card-text card-date"><small class="text-muted">{{posts[((i-1)*4)+x-1].date}}</small></p>
            </div>
        </div>
    </div>
</div>
</template>

<script>
export default {
    name:"Card",
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
.card-img-top{
    height: 230px;
}
.card-body{
    height: 230px;
    position: relative;
}
.card-content{
    text-align: left;
}
.card-date{
    position: absolute;
    bottom:10px
}
.card-hidden{
    visibility: hidden;
}
</style>