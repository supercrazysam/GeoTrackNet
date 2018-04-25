#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 16:43:49 2018

@author: vnguye04
"""

import numpy as np
import tensorflow as tf

l_embedding_sizes = [350,1050,30,72]

def sample_one_hot(prob_):
    prob = prob_/tf.tile(tf.reduce_sum(prob_,axis=1,keep_dims=True),
                               multiples=[1,tf.shape(prob_)[1]])
    cdv = tf.cumsum(prob,axis = 1, exclusive=False)
    cdv_ex = tf.cumsum(prob,axis = 1, exclusive=True)
    
    thresh = tf.tile(tf.random_uniform(shape=(tf.shape(prob)[0],1)),
                        multiples=[1,tf.shape(prob)[1]])
    
    less_equal = tf.less_equal(cdv_ex,thresh)
    greater = tf.greater(cdv,thresh)
    
    one_hot = tf.cast(tf.logical_and(less_equal,greater), tf.float32)
    return one_hot

def sample_from_max_logits(logit):
    logit_lat, logit_lon,logit_sog,logit_cog = tf.split(logit,l_embedding_sizes,axis=1)
    ind_lat = tf.argmax(logit_lat,axis = 1)
    ind_lon = tf.argmax(logit_lon,axis = 1)
    ind_sog = tf.argmax(logit_sog,axis = 1)
    ind_cog = tf.argmax(logit_cog,axis = 1)
    onehot_lat = tf.one_hot(ind_lat,500)
    onehot_lon = tf.one_hot(ind_lon,1000)
    onehot_sog = tf.one_hot(ind_sog,30)
    onehot_cog = tf.one_hot(ind_cog,72)
    fourhot = tf.concat([onehot_lat,onehot_lon,onehot_sog,onehot_cog],axis = 1)
    return fourhot
    
def sample_from_logits(logit):
    logit_lat, logit_lon,logit_sog,logit_cog = tf.split(logit,l_embedding_sizes,axis=1)
    dist_lat = tf.contrib.distributions.Bernoulli(logits=logit_lat)
    dist_lon = tf.contrib.distributions.Bernoulli(logits=logit_lon)
    dist_sog = tf.contrib.distributions.Bernoulli(logits=logit_sog)
    dist_cog = tf.contrib.distributions.Bernoulli(logits=logit_cog)
    sample_lat = dist_lat.sample()
    sample_lon = dist_lon.sample()
    sample_sog = dist_sog.sample()
    sample_cog = dist_cog.sample()
    sample_all = tf.concat([sample_lat,sample_lon,sample_sog,sample_cog],axis = 1)
    return sample_all
    
def sample_from_probs(probs_):
    def squash_prob(l_old_prob):
        l_new_probs = []
        for old_prob in l_old_prob:
            new_probs0 = old_prob/tf.reshape(tf.reduce_max(old_prob,axis=1),(-1,1))
            new_probs1 = tf.where(tf.equal(new_probs0,1.), tf.ones(tf.shape(old_prob))*0.9999, new_probs0)
            l_new_probs.append(new_probs1)
        return l_new_probs

    prob_lat, prob_lon,prob_sog,prob_cog = squash_prob(tf.split(probs_,l_embedding_sizes,axis=1))
    sample_lat = sample_one_hot(prob_lat)
    sample_lon = sample_one_hot(prob_lon)
    sample_sog = sample_one_hot(prob_sog)
    sample_cog = sample_one_hot(prob_cog)
    sample_all = tf.concat([sample_lat,sample_lon,sample_sog,sample_cog],axis = 1)
    return sample_all